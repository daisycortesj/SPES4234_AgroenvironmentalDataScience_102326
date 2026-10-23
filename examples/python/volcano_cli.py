#!/usr/bin/env python3
"""
volcano_cli.py — a volcano plot built "by hand" with numpy + matplotlib + argparse.

Adapted from a BME163 (UC Santa Cruz, Bioinformatics Visualization) assignment.
That course teaches matplotlib at the lowest level: you place every panel
yourself with plt.axes([left, bottom, width, height]) in figure-relative
units, and color every point yourself. It is more typing than seaborn,
but you control every pixel — useful for journal figures with strict sizes.

Changes from the original assignment:
  * reads a CSV with pandas instead of looping over a tab-separated file
  * uses padj from the CSV and thresholds you can change from the command line
  * no custom 'BME163' style sheet needed (the original required one)

Run from the repository's top folder:

    python examples/python/volcano_cli.py -i data/de_results.csv -o figures/volcano_cli.png
    python examples/python/volcano_cli.py -i data/de_results.csv -o figures/volcano_strict.png --fc 2 --padj 1e-10
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description="Volcano plot from a differential-expression table.")
parser.add_argument("-i", "--input_file", required=True)
parser.add_argument("-o", "--output_file", default="volcano.png")
parser.add_argument("--fc", type=float, default=1.0, help="|log2 fold change| threshold (default 1)")
parser.add_argument("--padj", type=float, default=0.05, help="adjusted p-value threshold (default 0.05)")
parser.add_argument("--n_labels", type=int, default=8, help="how many top genes to label")
args = parser.parse_args()

de = pd.read_csv(args.input_file)
x = de["log2FoldChange"].to_numpy()
y = -np.log10(de["padj"].to_numpy())
significant = (np.abs(x) > args.fc) & (de["padj"].to_numpy() < args.padj)

# --- figure with a hand-placed panel (the BME163 way) -------------------------
figure_width, figure_height = 3, 3          # inches
panel_width, panel_height = 2, 2            # inches
plt.figure(figsize=(figure_width, figure_height))
panel = plt.axes([0.5 / figure_width, 0.5 / figure_height,          # left, bottom (fraction of figure)
                  panel_width / figure_width, panel_height / figure_height])

panel.plot(x[~significant], y[~significant], marker="o", markersize=1.4, linewidth=0,
           markeredgewidth=0, markerfacecolor="black", alpha=0.4)
panel.plot(x[significant], y[significant], marker="o", markersize=1.4, linewidth=0,
           markeredgewidth=0, markerfacecolor="red")

for _, row in de.nsmallest(args.n_labels, "padj").iterrows():
    panel.text(row["log2FoldChange"], -np.log10(row["padj"]), row["gene"] + " ",
               fontsize=5, ha="right", va="center")

panel.set_xlabel("log$_2$(fold change)", fontsize=8)
panel.set_ylabel("-log$_{10}$(adjusted p-value)", fontsize=8)
panel.tick_params(labelsize=7)
panel.set_xlim(-8, 8)

Path(args.output_file).parent.mkdir(parents=True, exist_ok=True)
plt.savefig(args.output_file, dpi=600)
print(f"{significant.sum()} significant genes; saved {args.output_file}")
