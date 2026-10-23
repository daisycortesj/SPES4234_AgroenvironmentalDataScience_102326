"""
03 · INDEPENDENT PRACTICE  — SOLUTIONS

HOW TO RUN (from the repository folder, in a terminal):
    Mac:      python3 python/solutions/03_independent_practice_SOLUTION.py
    Windows:  python python/solutions/03_independent_practice_SOLUTION.py
    Plots open in their own window (A, then C, then B, then D). CLOSE each window to continue.
"""

import numpy as np                  # math (used for -log10 in Challenge D)
import pandas as pd                 # tables
import matplotlib.pyplot as plt     # plotting foundation
import seaborn as sns               # quick statistical plots

sns.set_theme(style="ticks", font_scale=1.3)

# Same site colors as the demo (color-blind friendly)
site_colors = {"Bottomland": "#0072B2", "Upland": "#E69F00"}


#######################################################
###          CHALLENGE A · Growth curves            ###
#######################################################
growth = pd.read_csv("data/growth_curves.csv")

# Step 1: average height for each day and nitrogen rate
#         .reset_index() turns the result back into a normal table
growth_means = (growth
                .groupby(["days_after_planting", "nitrogen_kg_ha"])["height_cm"]
                .mean()
                .reset_index())
print(growth_means.head())

# Step 2: one line per nitrogen rate
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(data=growth_means, x="days_after_planting", y="height_cm",
             hue="nitrogen_kg_ha",
             palette="viridis",             # color-blind-friendly colors
             legend="full",                 # show all 4 nitrogen rates in the legend
             marker="o", ax=ax)

# Step 3: labels with units and a title that states the finding
ax.set_xlabel("Days after planting")
ax.set_ylabel("Mean plant height (cm)")
ax.set_title("More nitrogen, taller plants")
ax.legend(title="N rate (kg/ha)")

# Step 4: save, then show
fig.tight_layout()                  # make room so no label gets cut off
fig.savefig("figures/growth_curves_python.png", dpi=300)
plt.show()


#######################################################
###        CHALLENGE C · Fix the ugly plot          ###
#######################################################
# Problems with the ugly plot:
# 1. Two different things (yield AND height / 20!) share one y-axis -> confusing.
# 2. No axis labels, no units, and the title "data" says nothing.
# 3. Big solid dots pile on top of each other (overplotting).
# 4. No legend: what do red and orange mean?
# 5. The figure is very wide and flat, which squashes the pattern.
# 6. It ignores site, which probably explains the pattern.
#
# The fix: ONE variable per plot, color by site, see-through dots, clear labels.

field = pd.read_csv("data/field_trial.csv")

# Step 1: remove the 3 plots with no yield
field_yield = field.dropna(subset=["yield_t_ha"])

# Steps 2-4: plot only yield, colored by site, see-through dots, clear labels
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=field_yield, x="soil_moisture_pct", y="yield_t_ha",
                hue="site", palette=site_colors,
                s=60,                       # dot size
                alpha=0.6,                  # see-through, so overlapping dots stay visible
                ax=ax)
ax.set_xlabel("Soil moisture (%)")
ax.set_ylabel("Grain yield (t/ha)")
ax.set_title("Wetter Bottomland plots tended to yield more")
ax.legend(title="Site")

# Step 5: save, then show
fig.tight_layout()                  # make room so no label gets cut off
fig.savefig("figures/moisture_fixed_python.png", dpi=300)
plt.show()

# Want height too? Make a SECOND plot: copy the code above and change
# y="yield_t_ha"  ->  y="plant_height_cm"   and the y label to "Plant height (cm)".


#######################################################
###            CHALLENGE B · Heatmap                ###
#######################################################
# Step 1: average yield for each variety and nitrogen rate.
#         .unstack() makes it WIDE: varieties as rows, nitrogen rates as columns.
yield_table = (field
               .groupby(["variety", "nitrogen_kg_ha"])["yield_t_ha"]
               .mean()
               .unstack())
print(yield_table.round(1))         # a 4 x 4 table of average yields

# Step 2: one colored square per combination, with the number written on it
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.heatmap(yield_table,
            annot=True,             # write the number in each square
            fmt=".1f",              # 1 decimal place
            cmap="YlGn",            # light yellow = low, dark green = high
            linewidths=0.5,         # thin white lines between squares
            cbar_kws={"label": "Mean yield (t/ha)"},
            ax=ax)
ax.set_xlabel("Nitrogen rate (kg N/ha)")
ax.set_ylabel("Variety")
ax.set_title("Mean yield by variety and nitrogen rate")

fig.tight_layout()                  # make room so no label gets cut off
fig.savefig("figures/yield_heatmap_python.png", dpi=300)
plt.show()

# HOW TO READ IT: darker green = higher yield. Every row gets darker from left to right
# (more nitrogen, more yield). The darkest square is Hybrid_D at 180 kg N/ha.


#######################################################
###           CHALLENGE D · Volcano plot            ###
#######################################################
# A volcano plot shows ALL genes at once:
#   x = how much a gene changed (log2 fold change): left = DOWN, right = UP in drought
#   y = how confident we are (-log10 adjusted p-value): higher = more significant

# Step 1: load the data
de = pd.read_csv("data/de_results.csv")

# Step 2: add two new columns
#   neg_log10_padj = the y-axis value (small p-values become BIG numbers)
#   result         = "Significant" if padj < 0.05 AND the gene changed more than 2-fold
de["neg_log10_padj"] = -np.log10(de["padj"])
de["result"] = "Not significant"
de.loc[(de["padj"] < 0.05) & (de["log2FoldChange"].abs() > 1), "result"] = "Significant"
print(de["result"].value_counts())  # how many genes in each group? (155 significant)

# Step 3: the plot
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=de, x="log2FoldChange", y="neg_log10_padj",
                hue="result",
                palette={"Not significant": "lightgray", "Significant": "firebrick"},
                s=15, alpha=0.7, linewidth=0, ax=ax)

# Step 4: dashed cutoff lines
ax.axhline(-np.log10(0.05), color="black", linestyle="--", linewidth=1)   # p = 0.05
ax.axvline(-1, color="black", linestyle="--", linewidth=1)                # 2-fold down
ax.axvline(1, color="black", linestyle="--", linewidth=1)                 # 2-fold up

# Step 5: label the 10 most significant genes
#   nsmallest(10, "padj") = the 10 rows with the smallest p-values
#   The for loop goes through those 10 rows one at a time and writes each gene name.
top_genes = de.nsmallest(10, "padj")
for _, row in top_genes.iterrows():
    ax.text(row["log2FoldChange"], row["neg_log10_padj"], " " + row["gene"], fontsize=9)

ax.set_xlabel("log2 fold change (drought vs control)")
ax.set_ylabel("-log10 adjusted p-value")
ax.set_title("Drought-responsive genes (simulated)")
ax.legend(title=None, loc="center")      # the middle of a volcano plot is empty

fig.tight_layout()                  # make room so no label gets cut off
fig.savefig("figures/volcano_python.png", dpi=300)
plt.show()

# Labels overlapping a bit? That's normal in volcano plots. In R, the ggrepel package
# moves labels apart automatically; in Python, the adjustText package does the same.

print("Done! All solutions finished.")