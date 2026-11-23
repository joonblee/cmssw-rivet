"""Overlay sample theory reports on an existing GEN-25-002 generator comparison."""
import argparse
import json
import re
import runpy
import shutil
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def draw_band(axis, edges, low, high, colour):
    axis.fill_between(edges, np.r_[low, low[-1]], np.r_[high, high[-1]],
                      step="post", color=colour, alpha=0.16, linewidth=0, zorder=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plot", type=Path, help="Paper figure/generator_comparison/.../dNN-xNN-yNN.py")
    parser.add_argument("--samples", type=Path, help="JSON mapping exact MC labels to theory JSON paths relative to the map")
    parser.add_argument("--list-samples", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("theory_plots"))
    args = parser.parse_args()
    plot = args.plot.resolve()
    figure = next(parent for parent in plot.parents if parent.name == "figure")
    archive = figure.with_name("figure_old") / plot.parent.relative_to(figure)
    datafile = next(p for folder in (plot.parent, archive)
                    for p in sorted(folder.glob(plot.stem + "__data*.py")))
    data = runpy.run_path(str(datafile))
    labels = set(data["yvals"]) - {"Data"}
    if args.list_samples:
        print(json.dumps(dict.fromkeys(sorted(labels), ""), indent=2))
        return
    if not args.samples:
        parser.error("Supply --samples or --list-samples")
    sources = json.loads(args.samples.read_text())
    if not sources or set(sources) - labels:
        parser.error("Use sample labels from --list-samples")
    observable = re.search(r"^# Analysis object: (\S+)", plot.read_text(), re.M)[1]
    destination = args.output.resolve() / observable.strip("/")
    destination.mkdir(parents=True, exist_ok=True)
    reports = {}
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        shutil.copy(plot, folder)
        styles = [plot.parent / "default.mplstyle", archive / "default.mplstyle"]
        style = next((s for s in styles if s.exists()), None)
        if style is None:
            style = next(figure.with_name("figure_old").rglob("default.mplstyle"))
        shutil.copy(style, folder)
        staged = folder / (plot.stem + "__data.py")
        shutil.copy(datafile, staged)
        with staged.open("a") as stream:
            for label, filename in sources.items():
                report = json.loads((args.samples.parent / filename).read_text())
                points = report["histograms"][observable]
                edges = np.asarray(data["xedges"][label])
                x = np.array([p["x"] for p in points])
                xl, xr = np.array([p["xerr"] for p in points]).T
                if len(x) + 1 != len(edges) or not (
                    np.allclose(x-xl, edges[:-1]) and np.allclose(x+xr, edges[1:])
                ):
                    raise ValueError(f"{label}: theory and paper bin edges differ")
                central = [p["y"] for p in points]
                stat = np.array([p["stat"] for p in points]).T.tolist()
                stream.write(f"\nyvals[{label!r}] = {central!r}\nyerrs[{label!r}] = {stat!r}\n")
                stream.write(f"variation_yvals = {{k:v for k,v in variation_yvals.items() if not k.startswith({label!r})}}\n")
                reports[label] = points
                for note in report.get("availability", []):
                    print(f"{label}: {note}")
        state = runpy.run_path(str(folder / plot.name),
                               init_globals={"YODA_USER_PLOT_PATH": str(folder)})
    fig, ax, ratio = (state[k] for k in ("fig", "ax", "ratio0_ax"))
    for label, points in reports.items():
        central = np.array([p["y"] for p in points])
        low, high = np.array([p["theory"] for p in points]).T
        edges = np.array(data["xedges"][label])
        integral = state["_integral_in_visible_range"](label, central)
        scale = state["data_integral"] / integral
        colour = state["styles"][label]["color"]
        lower, upper = scale * (central-low), scale * (central+high)
        draw_band(ax, edges, lower, upper, colour)
        ref = np.array(data["yvals"]["Data"])
        with np.errstate(divide="ignore", invalid="ignore"):
            draw_band(ratio, edges, np.where(ref != 0, lower/ref, np.nan),
                      np.where(ref != 0, upper/ref, np.nan), colour)
        component_fig, component_ax = plt.subplots(figsize=(8, 5))
        errors = {key: [p["components"][key] for p in points] for key in points[0]["components"]}
        errors["Total theory"] = [p["theory"] for p in points]
        for key, pair in errors.items():
            denom = np.where(central != 0, np.abs(central), np.nan)
            down, up = 100 * np.asarray(pair).T / denom
            line = component_ax.stairs(up, edges, label=key)
            component_ax.stairs(-down, edges, color=line.get_edgecolor(), linestyle="--")
        component_ax.set(xscale=ax.get_xscale(), xlim=ax.get_xlim(),
                         xlabel=ratio.get_xlabel(), ylabel="Relative uncertainty [%]")
        component_ax.axhline(0, color="grey", linewidth=.6)
        component_ax.legend(fontsize=9)
        component_ax.set_title(label, fontsize=9, wrap=True)
        component_fig.savefig(destination / (Path(label).stem + "_systematics.pdf"), bbox_inches="tight")
        plt.close(component_fig)
    ax.text(.98, .02, "Shading: total theory uncertainty", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=9)
    fig.savefig(destination / "comparison_theory.pdf", bbox_inches="tight", pad_inches=.02)
    plt.close(fig)


if __name__ == "__main__":
    main()
