"""
03 · INDEPENDENT PRACTICE (Python) 

IN CLASS, pick ONE challenge: A or C.
B and D are take-home (or for early finishers).
No blanks this time: YOU write the code. Copy and adapt code from
01_demo.py and 02_guided_exercise.py. That's how real programmers work!

    A  Growth curves over the season     data/growth_curves.csv   (in class)
    B  Heatmap of yield                   data/field_trial.csv     (take-home)
    C  Fix the ugly plot                  data/field_trial.csv     (take-home)
    D  Volcano plot of gene expression    data/de_results.csv      (take-home)

BEFORE YOU CALL IT DONE, check your figure:
    [ ] Could a reader tell what question it answers WITHOUT you explaining it?
    [ ] Axis labels have UNITS?
    [ ] Legend title makes sense (not "nitrogen_kg_ha")?
    [ ] Colors easy to tell apart (also for color-blind readers)?
    [ ] Saved with fig.savefig(...)?

HOW TO RUN (from the repository folder, in a terminal):
    Mac:      python3 python/03_independent_practice.py
    Windows:  python python/03_independent_practice.py
    Plots open in their own window. CLOSE the window to continue.
    TIP: the whole file runs every time. That's fine: just close the plot windows
         you're not working on.

Solutions: python/solutions/03_independent_practice_SOLUTION.py
"""

import pandas as pd                 # tables
import matplotlib.pyplot as plt     # plotting foundation
import seaborn as sns               # quick statistical plots

sns.set_theme(style="ticks", font_scale=1.3)

# Same site colors as the demo (color-blind friendly)
site_colors = {"Bottomland": "#0072B2", "Upland": "#E69F00"}


#######################################################
###     CHALLENGE A - Growth curves (in class)    ###
#######################################################
# QUESTION: How does plant height change over the season,
#           and does nitrogen change the growth curve?
#
# The data: plant height measured every week (14 to 98 days after planting).
# Columns: plot_id, site, variety, nitrogen_kg_ha, days_after_planting, height_cm
#
# STEPS:
# 1. Average the height for each day and nitrogen rate:
#        growth.groupby(["days_after_planting", "nitrogen_kg_ha"])["height_cm"].mean().reset_index()
#    (.reset_index() turns the result back into a normal table you can plot)
# 2. Plot it with sns.lineplot:
#        x = "days_after_planting", y = "height_cm", hue = "nitrogen_kg_ha"
#        palette="viridis" gives color-blind-friendly colors
# 3b. Before saving, add fig.tight_layout() so no label gets cut off
# 3. Add axis labels with units and a title that states what you see.
# 4. Save it: fig.savefig("figures/growth_curves_python.png", dpi=300)

growth = pd.read_csv("data/growth_curves.csv")
print(growth.head())

# your code here

#######################################################
###     CHALLENGE B - Heatmap (take-home)        ###
#######################################################
# QUESTION: Which variety x nitrogen combination gave the highest average yield?
#
# STEPS:
# 1. Average yield for each variety and nitrogen rate, as a wide table
#    (varieties as rows, nitrogen rates as columns):
#        field.groupby(["variety", "nitrogen_kg_ha"])["yield_t_ha"].mean().unstack()
# 2. Plot it:
#        sns.heatmap(your_table, annot=True, fmt=".1f", cmap="YlGn", ax=ax)
#        annot=True writes the number in each square; fmt=".1f" = 1 decimal place
# 3. Labels, title, save.

# your code here

#######################################################
###     CHALLENGE C - Fix the ugly plot (in class) ###
#######################################################
# The code below makes a BAD figure on purpose. Run it and look at it.
# 1. Write down at least 3 problems (as comments below).
# 2. Write a better version underneath.
#
# THINK ABOUT: Are two different things sharing one axis? Labels? Units? Title?
#              Do the dots hide each other? What do the colors mean? Is a group missing?

field = pd.read_csv("data/field_trial.csv")

fig, ax = plt.subplots(figsize=(9, 2))
ax.scatter(field["soil_moisture_pct"], field["yield_t_ha"], c="red", s=80)
ax.scatter(field["soil_moisture_pct"], field["plant_height_cm"] / 20, c="orange", s=80)
ax.set_title("data")
plt.show()

# Problems I see:
# 1.
# 2.
# 3.

# your improved version here



#######################################################
###     CHALLENGE D - Volcano plot (take-home)   ###
#######################################################
# QUESTION: Which genes change the most under drought? (SIMULATED RNA-seq results)
#
# Columns: gene, baseMean, log2FoldChange, pvalue, padj
#   x = log2FoldChange  (left = DOWN in drought, right = UP in drought)
#   y = -log10(padj)    (higher = more significant)
#
# STEPS:
# 1. Make the y-axis column. Hint: import numpy as np, then
#        de["neg_log10_padj"] = -np.log10(de["padj"])
# 2. Make a column that says which genes are significant:
#        de["result"] = "Not significant"
#        de.loc[(de["padj"] < 0.05) & (de["log2FoldChange"].abs() > 1), "result"] = "Significant"
# 3. sns.scatterplot(data=de, x=..., y=..., hue="result", ...)
#    Colors: palette={"Not significant": "lightgray", "Significant": "firebrick"}
# 4. Stretch: dashed cutoff lines with ax.axhline(...) and ax.axvline(...)
# 5. Stretch: label the 10 most significant genes (see the solution for how)

de = pd.read_csv("data/de_results.csv")
print(de.head())

# your code here


print("Done!")