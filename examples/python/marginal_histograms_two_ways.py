#!/usr/bin/env python3
"""
marginal_histograms_two_ways.py — the SAME figure made two ways.

Way 1: "by hand" with matplotlib (adapted from a BME163 assignment):
       place three panels yourself and draw every histogram bar as a Rectangle.
Way 2: seaborn's jointplot — one line.

Lesson: high-level libraries (seaborn, ggplot2) save time; low-level
matplotlib gives total control. Knowing both lets you pick the right tool.

Run from the repository's top folder:
    python examples/python/marginal_histograms_two_ways.py
Outputs: figures/marginal_by_hand.png and figures/marginal_seaborn.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mplpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

Path("figures").mkdir(exist_ok=True)
field = pd.read_csv("data/field_trial.csv").dropna(subset=["spad_chlorophyll", "yield_t_ha"])
x = field["spad_chlorophyll"].to_numpy()
y = field["yield_t_ha"].to_numpy()

# ---------------------------------------------------------------- Way 1: by hand
fig_w, fig_h = 4, 4
plt.figure(figsize=(fig_w, fig_h))
main = plt.axes([0.15, 0.12, 0.6, 0.6])      # [left, bottom, width, height] as fractions
top = plt.axes([0.15, 0.75, 0.6, 0.15])
side = plt.axes([0.78, 0.12, 0.15, 0.6])

main.plot(x, y, marker="o", linewidth=0, markersize=3, markeredgewidth=0,
          markerfacecolor="darkgreen", alpha=0.5)
main.set_xlabel("SPAD chlorophyll")
main.set_ylabel("Yield (t/ha)")

x_bins = np.linspace(x.min(), x.max(), 16)
y_bins = np.linspace(y.min(), y.max(), 16)
x_counts, _ = np.histogram(x, x_bins)
y_counts, _ = np.histogram(y, y_bins)

for i, count in enumerate(x_counts):                  # top histogram: one Rectangle per bar
    top.add_patch(mplpatches.Rectangle((x_bins[i], 0), x_bins[i + 1] - x_bins[i], count,
                                       facecolor="gray", edgecolor="black", linewidth=0.3))
for i, count in enumerate(y_counts):                  # side histogram: sideways bars
    side.add_patch(mplpatches.Rectangle((0, y_bins[i]), count, y_bins[i + 1] - y_bins[i],
                                        facecolor="gray", edgecolor="black", linewidth=0.3))

top.set_xlim(main.get_xlim()); top.set_ylim(0, x_counts.max() * 1.1)
side.set_ylim(main.get_ylim()); side.set_xlim(0, y_counts.max() * 1.1)
top.tick_params(labelbottom=False, bottom=False)
side.tick_params(labelleft=False, left=False)
plt.savefig("figures/marginal_by_hand.png", dpi=300)
plt.close()

# ---------------------------------------------------------------- Way 2: seaborn
g = sns.jointplot(data=field, x="spad_chlorophyll", y="yield_t_ha",
                  color="darkgreen", alpha=0.5, height=4, marginal_kws={"bins": 15})
g.set_axis_labels("SPAD chlorophyll", "Yield (t/ha)")
g.savefig("figures/marginal_seaborn.png", dpi=300)

print("Saved figures/marginal_by_hand.png and figures/marginal_seaborn.png")
