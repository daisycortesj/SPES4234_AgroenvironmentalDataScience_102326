#!/usr/bin/env python3
"""
quick_plot.py — make a scatter plot from ANY CSV file, from the command line.

Why does this exist? To show what `argparse` is for.
In a notebook you change values by editing code. In a script, `argparse`
lets you change values by typing options when you RUN the script — so the
same script can plot many files/columns without editing it. This is how
most bioinformatics tools (and HPC cluster jobs) work.

Try it (from the repository's top folder):

    python python/argparse_example/quick_plot.py --help

    python python/argparse_example/quick_plot.py \
        -i data/field_trial.csv -x spad_chlorophyll -y yield_t_ha \
        --hue site -o figures/spad_vs_yield.png

    python python/argparse_example/quick_plot.py \
        -i data/field_trial.csv -x soil_moisture_pct -y plant_height_cm \
        --title "Height vs soil moisture" -o figures/height_vs_moisture.png
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")            # draw to a file, no pop-up window (works on servers too)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 1. Describe the options the script accepts --------------------------------
parser = argparse.ArgumentParser(description="Scatter plot of two columns from a CSV file.")
parser.add_argument("-i", "--input_file", required=True, help="path to a .csv file")
parser.add_argument("-x", "--x_col", required=True, help="column for the x-axis")
parser.add_argument("-y", "--y_col", required=True, help="column for the y-axis")
parser.add_argument("--hue", default=None, help="(optional) column used to color points")
parser.add_argument("--title", default="", help="(optional) plot title")
parser.add_argument("-o", "--output_file", default="quick_plot.png", help="where to save (.png/.pdf/.svg)")
parser.add_argument("--dpi", type=int, default=300, help="resolution for .png files (default 300)")

# 2. Read what the user typed ---------------------------------------------------
args = parser.parse_args()

# 3. Use the values -------------------------------------------------------------
df = pd.read_csv(args.input_file)

for col in [args.x_col, args.y_col] + ([args.hue] if args.hue else []):
    if col not in df.columns:
        parser.error(f"column '{col}' not found. Available columns: {', '.join(df.columns)}")

sns.set_theme(style="ticks")
fig, ax = plt.subplots(figsize=(5, 4))
sns.scatterplot(data=df, x=args.x_col, y=args.y_col, hue=args.hue, alpha=0.7, ax=ax)
ax.set(title=args.title)
fig.tight_layout()

Path(args.output_file).parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output_file, dpi=args.dpi)
print(f"Saved {args.output_file}")
