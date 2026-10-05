import importlib.util
import json
import math
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace

import theory_uncertainties as theory


def point(value, x=0.5):
    return {"x": x, "xerr": [0.5, 0.5], "y": value, "stat": [2.0, 2.0]}


def metadata(weights=None, headers=None):
    return {"schema_version": 1, "preserve_variation_rate": True,
            "generator_weights": [{"name": "", "description": "nominal"}],
            "lhe_weights": weights or [], "lhe_headers": headers or []}


class TheoryTests(unittest.TestCase):
    def test_replica_mean_is_not_nominal_and_member0_excluded(self):
        # Nominal 100, replicas 80/90/100: STD about their mean 90 is 10.
        self.assertEqual(theory.pdf_error(100, [80, 90, 100], "replicas"), (10, 10))

    def test_hessian_asymmetry_and_90_percent_conversion(self):
        down, up = theory.pdf_error(100, [110, 97, 104, 92], "hessian")
        self.assertAlmostEqual(down, math.sqrt(73))
        self.assertAlmostEqual(up, math.sqrt(116))
        down90, up90 = theory.pdf_error(100, [110, 97, 104, 92], "hessian", 90)
        self.assertAlmostEqual(down90 / down, 1 / 1.6448536269514722)
        self.assertAlmostEqual(up90 / up, 1 / 1.6448536269514722)

    def test_symmetric_hessian(self):
        self.assertEqual(theory.pdf_error(100, [103, 96], "symmhessian"), (5, 5))

    def test_components_combination_retains_central_and_stat(self):
        groups = {"scale": {"method": "envelope", "weights": ["s1", "s2"]},
                  "pdf": {"method": "replicas", "weights": ["p1", "p2", "p3"]},
                  "alphas": {"method": "half_difference", "weights": ["a1", "a2"]},
                  "isr": {"method": "envelope", "weights": ["i1", "i2"]},
                  "fsr": {"method": "envelope", "weights": ["f1", "f2"]}}
        values = {"": 100, "s1": 90, "s2": 120, "p1": 80, "p2": 100, "p3": 120,
                  "a1": 96, "a2": 104, "i1": 95, "i2": 105, "f1": 92, "f2": 108}
        result = theory.calculate_histogram({k: [point(v)] for k, v in values.items()}, groups)[0]
        self.assertEqual(result["y"], 100)
        self.assertEqual(result["stat"], [2, 2])
        self.assertAlmostEqual(result["theory"][0], math.sqrt(605))
        self.assertAlmostEqual(result["theory"][1], math.sqrt(905))

    def test_zero_and_negative_nominal_values(self):
        self.assertEqual(theory.envelope(0, [-2, 3]), (2, 3))
        self.assertEqual(theory.envelope(-5, [-8, -1]), (3, 4))

    def test_xml_attributes_multiline_and_event_id_order(self):
        data = metadata([{"id": "2002", "name": "LHE_2002"}, {"id": "2001", "name": "LHE_2001"}],
            [{"tag": "initrwgt", "text": "<weightgroup name='PDF variation' combine='hessian'>\n"
              "<weight id='2001' PDF='325301'>\n first member </weight>"
              "<weight id='2002'> lhapdf=325302 </weight></weightgroup>"}])
        result = theory.weight_inventory(data)
        self.assertEqual(result[1]["id"], "2002")
        self.assertEqual(result[2]["attributes"]["PDF"], "325301")
        self.assertEqual(theory.number(result[2], ["pdf"]), 325301)
        self.assertEqual(result[1]["group"]["combine"], "hessian")

    def test_complete_scale_group_excludes_anticorrelated_points(self):
        inventory = [{"name": "", "description": "", "source": "generator", "group": {}}]
        for r in (0.5, 1.0, 2.0):
            for f in (0.5, 1.0, 2.0):
                inventory.append({"name": "%s_%s" % (r, f), "description": "muR=%s muF=%s" % (r, f),
                                  "source": "lhe", "group": {"name": "scale variation"}})
        groups, _ = theory.discover_groups(inventory)
        self.assertEqual(len(groups["scale"]["weights"]), 6)
        self.assertNotIn("0.5_2.0", groups["scale"]["weights"])
        self.assertNotIn("2.0_0.5", groups["scale"]["weights"])
        self.assertNotIn("1.0_1.0", groups["scale"]["weights"])
        groups, report = theory.discover_groups(inventory[:-1])
        self.assertNotIn("scale", groups)
        self.assertTrue(any("scale unavailable" in r for r in report))

    def test_ps_only_standard_inclusive_factor_pair(self):
        descriptions = ["isr:muRfac=0.5", "isr:muRfac=2.0", "fsr:muRfac=0.5", "fsr:muRfac=2.0",
                        "isr:muRfac=0.25", "fsr:G2GG:muRfac=0.5", "fsr:muRfac=4.0"]
        inventory = [{"name": "w" + str(i), "source": "generator", "description": d, "group": {}}
                     for i, d in enumerate(descriptions)]
        groups, _ = theory.discover_groups(inventory)
        self.assertEqual(groups["isr"]["weights"], ["w0", "w1"])
        self.assertEqual(groups["fsr"]["weights"], ["w2", "w3"])

    def test_missing_weights_not_zero_uncertainty(self):
        group = {"scale": {"method": "envelope", "weights": ["missing"]}}
        with self.assertRaisesRegex(ValueError, "Missing histogram"):
            theory.calculate_histogram({"": [point(100)]}, group)
        with self.assertRaisesRegex(ValueError, "Unknown weight"):
            theory.validate_groups(group, [{"name": ""}])

    def test_binning_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, "binning"):
            theory.calculate_histogram({"": [point(100)], "v": [point(110, 1.5)]},
                                       {"scale": {"method": "envelope", "weights": ["v"]}})

    def test_duplicate_components_rejected(self):
        with self.assertRaisesRegex(ValueError, "both"):
            theory.validate_groups({"pdf": {"method": "symmhessian", "weights": ["p"]},
                                    "alphas": {"method": "envelope", "weights": ["p"]}},
                                   [{"name": ""}, {"name": "p"}])

    def test_metadata_compatibility_and_old_normalisation(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a.json", Path(tmp) / "b.json"
            a.write_text(json.dumps(metadata()))
            other = metadata()
            other["lhe_weights"] = [{"id": "1", "name": "LHE_1"}]
            b.write_text(json.dumps(other))
            with self.assertRaisesRegex(ValueError, "Incompatible"):
                theory.load_metadata([a, b])
            other["preserve_variation_rate"] = False
            b.write_text(json.dumps(other))
            with self.assertRaisesRegex(ValueError, "preserve"):
                theory.load_metadata([b])

    def test_pdf_ensemble_uses_metadata_and_rejects_incomplete(self):
        class PDFLibrary:
            @staticmethod
            def lookupPDF(wid):
                return "TestPDF", wid - 100
            @staticmethod
            def getPDFSet(name):
                return SimpleNamespace(size=3, errorType="symmhessian")
        inventory = [{"name": "p" + str(i), "source": "lhe", "description": "lhapdf=" + str(100 + i),
                      "group": {"name": "PDF variation"}} for i in range(3)]
        groups, _ = theory.discover_groups(inventory, PDFLibrary)
        self.assertEqual(groups["pdf:TestPDF"]["weights"], ["p0", "p1", "p2"])
        groups, _ = theory.discover_groups(inventory[1:], PDFLibrary)
        self.assertNotIn("pdf:TestPDF", groups)
        groups, _ = theory.discover_groups(inventory[1:], PDFLibrary, "TestPDF")
        self.assertEqual(groups["pdf:TestPDF"]["weights"], ["", "p1", "p2"])

    def test_generator_lhe_copies_are_not_counted_twice(self):
        class PDFLibrary:
            @staticmethod
            def lookupPDF(wid):
                return "TestPDF", wid - 100
            @staticmethod
            def getPDFSet(name):
                return SimpleNamespace(size=3, errorType="symmhessian")
        inventory = []
        for i in range(3):
            inventory += [{"name": "GEN_" + str(i), "source": "generator",
                           "description": "group = PDF variation, lhapdf=" + str(100 + i), "group": {}},
                          {"name": "LHE_" + str(i), "source": "lhe", "description": "lhapdf=" + str(100 + i),
                           "group": {"name": "PDF variation"}}]
        for r, f in sorted(theory.SCALE_POINTS):
            inventory += [{"name": "GEN_%s_%s" % (r, f), "source": "generator",
                           "description": "group = scale variation, muR=%s muF=%s" % (r, f), "group": {}},
                          {"name": "LHE_%s_%s" % (r, f), "source": "lhe",
                           "description": "muR=%s muF=%s" % (r, f), "group": {"name": "scale variation"}}]
        groups, _ = theory.discover_groups(inventory, PDFLibrary)
        self.assertTrue(all(w.startswith("LHE_") for g in groups.values() for w in g["weights"]))
        groups, _ = theory.discover_groups([i for i in inventory if i["source"] == "generator"], PDFLibrary)
        self.assertIn("scale", groups)
        self.assertIn("pdf:TestPDF", groups)

    def test_lhapdf_64_metadata_lookup_and_parameter_api(self):
        class LegacyPDFLibrary:
            @staticmethod
            def availablePDFSets():
                return ["TestPDF"]
            @staticmethod
            def getPDFSet(name):
                return SimpleNamespace(size=5, lhapdfID=100, errorType="symmhessian+as",
                    uncertainty=lambda values, cl: SimpleNamespace(central=100, errminus_pdf=5,
                                                                    errplus_pdf=5, err_par=4))
        self.assertEqual(theory.lookup_pdf(LegacyPDFLibrary, 103, {}), ("TestPDF", 3))
        group = {"pdf:TestPDF": {"method": "lhapdf", "set": "TestPDF", "weights": ["", "e1", "e2", "a1", "a2"]}}
        values = {"": 100, "e1": 103, "e2": 96, "a1": 96, "a2": 104}
        result = theory.calculate_histogram({k: [point(v)] for k, v in values.items()}, group, LegacyPDFLibrary)[0]
        self.assertEqual(result["components"]["alphas:TestPDF"], [4, 4])
        self.assertAlmostEqual(result["theory"][0], math.sqrt(41))
        group["pdf:TestPDF"]["alphas_rescale"] = 0.5
        result = theory.calculate_histogram({k: [point(v)] for k, v in values.items()}, group, LegacyPDFLibrary)[0]
        self.assertEqual(result["components"]["alphas:TestPDF"], [2, 2])
        self.assertTrue(theory.has_alphas(SimpleNamespace(errorType="replicas+alphas")))

    def test_path_weight_is_suffix(self):
        self.assertEqual(theory.split_weight_path("/CMS/d01-x01-y01[LHE_1002]"),
                         ("/CMS/d01-x01-y01", "LHE_1002"))

    @unittest.skipUnless(importlib.util.find_spec("yoda"), "Requires native YODA Python bindings")
    def test_native_discrete_histogram(self):
        import yoda
        histogram = yoda.Histo1D([0, 1, 2])
        histogram.fill(0, 3)
        self.assertIsNotNone(theory.scatter_points(histogram, yoda))

    @unittest.skipUnless(importlib.util.find_spec("yoda"), "Requires native YODA Python bindings")
    def test_native_yoda_end_to_end_with_bin_width(self):
        import yoda
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            objects = []
            for weight, value in [("", 100), ("LHE_1", 90), ("LHE_2", 120)]:
                histogram = yoda.Histo1D([0.0, 2.0])
                histogram.setPath("/MC_TEST/h" + ("[" + weight + "]" if weight else ""))
                histogram.fill(1.0, value)
                objects.append(histogram)
            yoda.write(objects, str(tmp / "input.yoda"))
            data = metadata([{"id": "1", "name": "LHE_1"}, {"id": "2", "name": "LHE_2"}])
            (tmp / "weights.json").write_text(json.dumps(data))
            (tmp / "groups.json").write_text(json.dumps({"scale": {"method": "envelope", "weights": ["LHE_1", "LHE_2"]}}))
            rc = theory.main([str(tmp / "input.yoda"), "--metadata", str(tmp / "weights.json"),
                              "--groups", str(tmp / "groups.json"), "--output", str(tmp / "theory")])
            self.assertEqual(rc, 0)
            result = json.loads((tmp / "theory.json").read_text())["histograms"]["/MC_TEST/h"][0]
            self.assertEqual(result["y"], 50)  # histogram height = 100 / width 2
            self.assertEqual(result["theory"], [5, 10])
            band = yoda.read(str(tmp / "theory.yoda"))["/MC_TEST/h"]
            self.assertEqual(tuple(band.points()[0].yErrs()), (5, 10))


if __name__ == "__main__":
    unittest.main()
