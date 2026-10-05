#!/usr/bin/env python3
"""Build theory bands from a merged Rivet YODA file and CRAB weight metadata.

Run in the CMSSW/Rivet environment, with the YODA and LHAPDF Python bindings.
No weights are guessed from their vector positions or numerical LHE IDs.
"""

import argparse
import csv
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ONE_SIGMA_CL = 68.26894921370858
SCALE_POINTS = {(0.5, 0.5), (0.5, 1.0), (1.0, 0.5),
                (1.0, 2.0), (2.0, 1.0), (2.0, 2.0)}


def has_alphas(pdf):
    return pdf.errorType.split("+")[1:] in (["as"], ["alphas"])


def envelope(central, variations):
    if not variations:
        raise ValueError("An envelope requires variation values")
    return max(0.0, central - min(variations)), max(0.0, max(variations) - central)


def pdf_error(central, values, prescription, confidence_level=ONE_SIGMA_CL):
    """Explicit-manifest PDF prescriptions; auto mode delegates to LHAPDF.

    Replicas use the sample standard deviation about the replica mean, excluding
    member 0. The nominal event-generator prediction remains the plotted centre.
    Hessian values are ordered eigenvector +/- pairs; symmhessian has one per EV.
    """
    if prescription == "replicas":
        if len(values) < 2:
            raise ValueError("At least two PDF replicas are required")
        mean = sum(values) / len(values)
        error = math.sqrt(sum((v - mean) ** 2 for v in values) / (len(values) - 1))
        return error, error
    if prescription == "symmhessian":
        error = math.sqrt(sum((v - central) ** 2 for v in values))
        down, up = error, error
    elif prescription == "hessian":
        if len(values) % 2 or not values:
            raise ValueError("Hessian members must be ordered +/- pairs")
        pairs = list(zip(values[::2], values[1::2]))
        up = math.sqrt(sum(max(a - central, b - central, 0.0) ** 2 for a, b in pairs))
        down = math.sqrt(sum(max(central - a, central - b, 0.0) ** 2 for a, b in pairs))
    else:
        raise ValueError("Unknown PDF prescription: " + prescription)
    if not values:
        raise ValueError("No PDF error members")
    # Convert the usual 90% CL Hessian sets to 68.268949% CL.
    from statistics import NormalDist
    if not 0 < confidence_level < 100:
        raise ValueError("PDF confidence level must be between 0 and 100")
    scale = 1.0 / NormalDist().inv_cdf((1.0 + confidence_level / 100.0) / 2.0)
    return down * scale, up * scale


def load_metadata(paths):
    if not paths:
        raise ValueError("Supply all output.weights.json files for the merged sample")
    records = [json.loads(Path(p).read_text()) for p in paths]
    first = records[0]
    if first.get("schema_version") != 1:
        raise ValueError("Unsupported metadata schema")
    for path, record in zip(paths[1:], records[1:]):
        if record != first:
            raise ValueError("Incompatible weight definitions: " + str(path))
    if not first.get("preserve_variation_rate"):
        raise ValueError("Input did not preserve variation rates; rerun with preserveVariationRate=True")
    return first


def weight_inventory(metadata):
    definitions = {}
    for header in metadata.get("lhe_headers", []):
        text = header["text"]
        try:
            root = ET.fromstring("<root>" + text + "</root>")
        except ET.ParseError as exc:
            raise ValueError("Cannot parse LHE reweighting XML: " + str(exc)) from exc

        def walk(node, group=None):
            if node.tag == "weightgroup":
                group = dict(node.attrib)
            if node.tag == "weight" and "id" in node.attrib:
                wid = node.attrib["id"]
                value = {"description": " ".join("".join(node.itertext()).split()),
                         "attributes": dict(node.attrib), "group": group or {}}
                if wid in definitions and definitions[wid] != value:
                    raise ValueError("Conflicting LHE definitions for ID " + wid)
                definitions[wid] = value
            for child in node:
                walk(child, group)
        walk(root)
    inventory = []
    for item in metadata.get("generator_weights", []):
        inventory.append(dict(item, source="generator", attributes={}, group={}))
    for item in metadata.get("lhe_weights", []):
        inventory.append(dict(item, source="lhe", **definitions.get(item["id"],
                              {"description": "", "attributes": {}, "group": {}})))
    names = [item["name"] for item in inventory]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate weight names")
    return inventory


def number(item, aliases):
    text = item.get("description", "") + " " + " ".join(
        k + "=" + str(v) for k, v in item.get("attributes", {}).items())
    for alias in aliases:
        match = re.search(r"(?<![A-Za-z0-9])" + alias + r"\s*=\s*([0-9.eE+\-]+)", text, re.I)
        if match:
            return float(match.group(1))
        match = re.search(r"(?:^|_)" + alias + r"([0-9.]+)(?:_|$)", text, re.I)
        if match:
            return float(match.group(1))
    return None


def lookup_pdf(lhapdf, pdfid, cache):
    if hasattr(lhapdf, "lookupPDF"):
        return lhapdf.lookupPDF(pdfid)
    # LHAPDF 6.4 has no Python lookupPDF binding. Read the installed set
    # metadata instead; getPDFSet does not instantiate/load member grids.
    if not cache:
        for name in lhapdf.availablePDFSets():
            pdf = lhapdf.getPDFSet(name)
            if pdf.lhapdfID >= 0:
                for member in range(pdf.size):
                    cache[pdf.lhapdfID + member] = (name, member)
        cache[-1] = ("", -1)  # mark initialised, including an empty installation
    if pdfid not in cache:
        raise ValueError("No installed set metadata for LHAPDF ID " + str(pdfid))
    return cache[pdfid]


def discover_groups(inventory, lhapdf=None, pdf_set=None):
    """Return complete identifiable groups and an explicit availability report."""
    report = []
    groups = {}
    scale_candidates = {}
    pdf_members = {}
    pdf_priority = {}
    pdf_cache = {}
    alpha_candidates = {}
    ps = {"isr": {}, "fsr": {}}
    for item in inventory:
        if not item["name"]:
            continue
        mur = number(item, ["muR", "renscfact"])
        muf = number(item, ["muF", "facscfact"])
        pdfid = number(item, ["lhapdf", "pdf", "pdfset"])
        group_text = " ".join(str(v) for v in item.get("group", {}).values())
        if not group_text:
            match = re.search(r"group\s*=\s*([^,]+)", item.get("description", ""), re.I)
            if match:
                group_text = match.group(1)
        rank = 2 if item["source"] == "lhe" else 1
        if mur is not None and muf is not None:
            key = (group_text, pdfid, rank)
            point = (mur, muf)
            if point in SCALE_POINTS or point == (1.0, 1.0):
                candidate = scale_candidates.setdefault(key, {})
                if point in candidate and candidate[point] != item["name"]:
                    report.append("Ambiguous duplicate scale point in group " + str(key))
                    candidate[point] = None
                else:
                    candidate[point] = item["name"]
        # PDF weights with varying ME scales must not enter the PDF ensemble.
        if pdfid is not None and mur in (None, 1.0) and muf in (None, 1.0):
            if lhapdf is not None:
                try:
                    setname, member = lookup_pdf(lhapdf, int(pdfid), pdf_cache)
                    if not setname:
                        raise ValueError("Unknown LHAPDF ID")
                    members = pdf_members.setdefault(setname, {})
                    priority = rank + (2 if re.search(r"pdf", group_text, re.I) else 0)
                    priorities = pdf_priority.setdefault(setname, {})
                    if member in members and priorities[member] == priority and members[member] != item["name"]:
                        # Two streams for the same member require an explicit choice.
                        members[member] = None
                    elif member not in members or priority > priorities[member]:
                        members[member] = item["name"]
                        priorities[member] = priority
                except (RuntimeError, ValueError) as exc:
                    report.append("Unresolved LHAPDF ID %s: %s" % (int(pdfid), exc))
            else:
                report.append("LHAPDF unavailable: PDF ID " + str(int(pdfid)))
        if re.search(r"alpha[_ ]?s", group_text, re.I):
            alpha_candidates.setdefault(rank, {}).setdefault(group_text, []).append(item["name"])
        desc = item.get("description", "")
        for shower in ps:
            # Only the inclusive muR factor variation, not splitting-kernel/cNS variations.
            match = re.fullmatch(r"\s*" + shower + r"[:_]muRfac\s*=\s*([0-9.]+)\s*", desc, re.I)
            aliases = {shower + "DefHi": 0.5, shower + "DefLo": 2.0}
            factor = float(match.group(1)) if match else aliases.get(desc.strip())
            if factor in (0.5, 2.0):
                if factor in ps[shower]:
                    ps[shower][factor] = None
                else:
                    ps[shower][factor] = item["name"]

    complete = [(key[2], v) for key, v in scale_candidates.items()
                if all(v.get(p) for p in SCALE_POINTS)]
    if complete:
        rank = max(r for r, _ in complete)
        complete = [v for r, v in complete if r == rank]
    if len(complete) == 1:
        groups["scale"] = {"method": "envelope", "weights": [complete[0][p] for p in sorted(SCALE_POINTS)]}
    else:
        report.append("scale unavailable/ambiguous: need one complete six-variation (7-point) group; found %d" % len(complete))

    for setname, members in sorted(pdf_members.items()):
        if pdf_set and setname != pdf_set:
            continue
        pdf = lhapdf.getPDFSet(setname)
        # Using nominal as member 0 is allowed only after an explicit --pdf-set declaration.
        if 0 not in members and pdf_set == setname:
            members[0] = ""
        if not all(i in members and members[i] is not None for i in range(pdf.size)):
            report.append("Incomplete/ambiguous PDF ensemble %s: %d of %d members" % (setname, len(members), pdf.size))
            continue
        method = pdf.errorType
        if method not in ("replicas", "hessian", "symmhessian",
                          "replicas+alphas", "hessian+alphas", "symmhessian+alphas",
                          "replicas+as", "hessian+as", "symmhessian+as"):
            report.append("Unsupported composite PDF prescription %s: %s" % (setname, method))
            continue
        groups["pdf:" + setname] = {"method": "lhapdf", "set": setname,
                                  "weights": [members[i] for i in range(pdf.size)]}
    if not any(k.startswith("pdf:") for k in groups):
        report.append("PDF unavailable: need a complete identified ensemble (or explicit manifest)")
    # A combined PDF+alphas set is handled by LHAPDF once; never add its pair twice.
    if not any(has_alphas(lhapdf.getPDFSet(g["set"]))
               for g in groups.values() if g["method"] == "lhapdf"):
        candidates = alpha_candidates.get(max(alpha_candidates), {}) if alpha_candidates else {}
        pairs = [v for v in candidates.values() if len(v) == 2]
        if len(pairs) == 1:
            groups["alphas"] = {"method": "half_difference", "weights": pairs[0]}
        else:
            report.append("alpha_s unavailable/ambiguous: no unique identified two-weight pair")
    for shower, weights in ps.items():
        if all(weights.get(f) for f in (0.5, 2.0)):
            groups[shower] = {"method": "envelope", "weights": [weights[0.5], weights[2.0]]}
        else:
            report.append(shower.upper() + " unavailable: no identified muR factors 0.5/2 pair")
    return groups, sorted(set(report))


def validate_groups(groups, inventory):
    known = {i["name"] for i in inventory}
    used = {}
    for key, group in groups.items():
        if group.get("central", "") not in known:
            raise ValueError("Unknown central weight for " + key)
        if not group.get("weights") or len(group["weights"]) != len(set(group["weights"])):
            raise ValueError("Empty/duplicate member list for " + key)
        for name in group["weights"]:
            if name not in known:
                raise ValueError("Unknown weight %r in %s" % (name, key))
            if name and name in used:
                raise ValueError("Weight %s appears in both %s and %s" % (name, used[name], key))
            if name:
                used[name] = key
        if group["method"] == "half_difference" and len(group["weights"]) != 2:
            raise ValueError("alpha_s half-difference requires exactly two weights")
        if not math.isfinite(group.get("rescale", 1.0)) or group.get("rescale", 1.0) <= 0:
            raise ValueError("alpha_s rescale must be positive and finite")
        if not math.isfinite(group.get("alphas_rescale", 1.0)) or group.get("alphas_rescale", 1.0) <= 0:
            raise ValueError("alpha_s rescale must be positive and finite")
        if group["method"] not in ("envelope", "half_difference", "replicas", "hessian", "symmhessian", "lhapdf"):
            raise ValueError("Unsupported method for " + key)


def split_weight_path(path):
    match = re.fullmatch(r"(.*)\[([^\[\]]*)\]", path)
    return (match.group(1), match.group(2)) if match else (path, "")


def scatter_points(obj, yoda):
    typename = obj.type()
    numeric_binned_1d = re.fullmatch(r"Binned(?:Histo|Profile|Estimate)<[id]>", typename)
    if typename not in ("Histo1D", "Profile1D", "Scatter2D", "Estimate1D") and not numeric_binned_1d:
        return None
    # Use YODA's conversion for density/bin-width conventions and profile means.
    scatter = obj if typename == "Scatter2D" else obj.mkScatter()
    return [{"x": p.x(), "xerr": list(p.xErrs()), "y": p.y(), "stat": list(p.yErrs())}
            for p in scatter.points()]


def same_binning(left, right):
    return len(left) == len(right) and all(
        all(math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12)
            for a, b in zip([p["x"]] + p["xerr"], [q["x"]] + q["xerr"]))
        for p, q in zip(left, right))


def calculate_histogram(streams, groups, lhapdf=None):
    central = streams[""]
    required = {name for group in groups.values() for name in group["weights"]}
    required.update(group.get("central", "") for group in groups.values())
    for name in required:
        if name not in streams:
            raise ValueError("Missing histogram weight stream: " + name)
        if not same_binning(central, streams[name]):
            raise ValueError("Incompatible variation binning: " + name)
    result = []
    for i, point in enumerate(central):
        c = point["y"]
        components = {}
        pdf_centres = {}
        for key, group in groups.items():
            values = [streams[name][i]["y"] for name in group["weights"]]
            if not all(math.isfinite(v) for v in values + [c]):
                raise ValueError("Non-finite central or variation value in bin " + str(i))
            method = group["method"]
            if method == "envelope":
                error = envelope(c, values)
            elif method == "half_difference":
                delta = abs(values[0] - values[1]) / 2 * group.get("rescale", 1.0)
                error = delta, delta
            elif method == "lhapdf":
                if lhapdf is None:
                    raise ValueError("LHAPDF Python bindings are required for " + key)
                pdf = lhapdf.getPDFSet(group["set"])
                uncertainty = pdf.uncertainty(values, ONE_SIGMA_CL)
                error = uncertainty.errminus_pdf, uncertainty.errplus_pdf
                pdf_centres[key] = uncertainty.central
                if has_alphas(pdf):
                    # LHAPDF 6.4 exposes only symmetric err_par; newer bindings
                    # expose separate parameter errors as well.
                    if hasattr(uncertainty, "errminus_par"):
                        alpha_error = [uncertainty.errminus_par, uncertainty.errplus_par]
                    else:
                        alpha_error = [uncertainty.err_par, uncertainty.err_par]
                    components["alphas:" + group["set"]] = [v * group.get("alphas_rescale", 1.0) for v in alpha_error]
            else:
                reference = streams[group.get("central", "")][i]["y"]
                error = pdf_error(reference, values, method, group.get("confidence_level", ONE_SIGMA_CL))
            components[key] = list(error)
        # Alternative PDF sets are separate predictions, never independent errors.
        pdfkeys = [k for k in components if k.startswith("pdf:") or k == "pdf"]
        if len(pdfkeys) > 1:
            raise ValueError("Multiple PDF ensembles: select one with --pdf-set or a manifest before combining")
        total = [math.sqrt(sum(err[j] ** 2 for err in components.values())) for j in (0, 1)]
        result.append(dict(point, components=components, theory=total, pdf_centres=pdf_centres))
    return result


def write_results(prefix, histograms, groups, report, skipped, include_stat, yoda):
    path = Path(prefix)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"groups": groups, "availability": report, "skipped_objects": skipped,
              "combination": "quadrature; independent-component convention, not a confidence interval",
              "statistical_errors_in_band": include_stat, "histograms": histograms}
    Path(str(path) + ".json").write_text(json.dumps(record, indent=2, allow_nan=False) + "\n")
    with open(str(path) + ".csv", "w", newline="") as stream:
        out = csv.writer(stream)
        out.writerow(["path", "bin", "x", "central", "component", "down", "up"])
        for name, points in histograms.items():
            for i, point in enumerate(points):
                for component, error in dict(point["components"], theory=point["theory"], stat=point["stat"]).items():
                    out.writerow([name, i, point["x"], point["y"], component, *error])
    bands = []
    for name, points in histograms.items():
        band = yoda.Scatter2D()
        band.setPath(name)
        band.setAnnotation("TheoryComponents", ",".join(sorted(groups)))
        band.setAnnotation("TheoryAvailability", "; ".join(report))
        for point in points:
            error = point["theory"]
            if include_stat:
                error = [math.hypot(error[j], point["stat"][j]) for j in (0, 1)]
            band.addPoint(point["x"], point["y"], *point["xerr"], *error)
        bands.append(band)
    yoda.write(bands, str(path) + ".yoda")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="Merged YODA output for ONE sample")
    parser.add_argument("--metadata", nargs="+", required=True, help="All job metadata files belonging to this sample")
    parser.add_argument("--pdf-set", help="Select one LHAPDF set; also declares nominal matches member 0 if that weight is absent")
    parser.add_argument("--groups", help="Explicit JSON group manifest (replaces automatic groups)")
    parser.add_argument("--list", action="store_true", help="Inspect weights and proposed groups without reading YODA")
    parser.add_argument("--output", default="theory", help="Output prefix for JSON, CSV and YODA bands")
    parser.add_argument("--include-stat", action="store_true", help="Include nominal MC statistical errors in plotted band")
    parser.add_argument("--alphas-rescale", type=float, default=1.0,
                        help="Rescale stored alpha_s errors (e.g. 0.5 converts +/-0.002 to +/-0.001 under linear response)")
    parser.add_argument("--require", nargs="*", default=[], choices=["scale", "pdf", "alphas", "isr", "fsr"],
                        help="Fail if any requested component is unavailable")
    args = parser.parse_args(argv)
    try:
        metadata = load_metadata(args.metadata)
        inventory = weight_inventory(metadata)
        try:
            import lhapdf
        except ImportError:
            lhapdf = None
        groups, report = discover_groups(inventory, lhapdf, args.pdf_set)
        if args.groups:
            groups = json.loads(Path(args.groups).read_text())
            report = ["Explicit user-supplied group manifest; check prescriptions against production metadata"]
        for key, group in groups.items():
            if group["method"] == "lhapdf":
                group["alphas_rescale"] = group.get("alphas_rescale", 1.0) * args.alphas_rescale
            elif key.split(":")[0] == "alphas":
                group["rescale"] = group.get("rescale", 1.0) * args.alphas_rescale
        validate_groups(groups, inventory)
        if args.list:
            print(json.dumps({"weights": inventory, "groups": groups, "availability": report}, indent=2))
            return 0
        if not args.input:
            raise ValueError("A merged YODA input is required without --list")
        available = {key.split(":")[0] for key in groups}
        if lhapdf:
            if any(has_alphas(lhapdf.getPDFSet(g["set"]))
                   for g in groups.values() if g["method"] == "lhapdf"):
                available.add("alphas")
        missing = set(args.require) - available
        if missing:
            raise ValueError("Required uncertainties unavailable: " + ", ".join(sorted(missing)))
        if not groups:
            raise ValueError("No identifiable uncertainty groups; inspect --list and provide --groups if necessary")
        import yoda
        objects = yoda.read(args.input)
        streams = {}
        skipped = []
        for name, obj in objects.items():
            if name.startswith(("/RAW/", "/REF/")) or "/TMP/" in name or name.startswith("/_"):
                continue
            base, weight = split_weight_path(name)
            points = scatter_points(obj, yoda)
            if points is None:
                skipped.append({"path": name, "reason": "Unsupported object type: " + obj.type()})
                continue
            if weight in streams.setdefault(base, {}):
                raise ValueError("Duplicate histogram stream: " + name)
            streams[base][weight] = points
        results = {}
        for name, weights in streams.items():
            if "" not in weights:
                skipped.append({"path": name, "reason": "No nominal stream"})
                continue
            results[name] = calculate_histogram(weights, groups, lhapdf)
        if not results:
            raise ValueError("No supported finalised histograms found")
        write_results(args.output, results, groups, report, skipped, args.include_stat, yoda)
        print("Calculated %d histograms; components: %s" % (len(results), ", ".join(groups)))
        for message in report:
            print("Availability: " + message, file=sys.stderr)
        print("Wrote %s.{json,csv,yoda}" % args.output)
        return 0
    except (ValueError, RuntimeError, OSError, ImportError, KeyError) as exc:
        print("Error: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
