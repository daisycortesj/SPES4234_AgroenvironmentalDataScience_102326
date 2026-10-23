"""
01 · LIVE DEMO — Plotting a Field Trial in Python

Question: Does nitrogen fertilizer increase maize yield,
          and is the response the same at both sites?

Data: data/field_trial.csv (SIMULATED maize trial, 192 plots)

HOW TO RUN (from the repository folder, in a terminal):
    Mac:      python3 python/01_demo.py
    Windows:  python python/01_demo.py
    (Using Anaconda or a virtual environment? Activate it first, then use "python".)
Each plot opens in its own window. CLOSE the window to continue to the next plot.

Lines starting with # are COMMENTS: notes for humans. Python ignores them.
"""

#######################################################
###             1. LOAD THE PACKAGES                ###
#######################################################
print("Starting the demo...")

import pandas as pd                 # tables (like dplyr in R)
import matplotlib.pyplot as plt     # the foundation of Python plotting
import seaborn as sns               # quick statistical plots, built on matplotlib

sns.set_theme(style="ticks", font_scale=1.3)    # cleaner look, bigger text for slides

# Same colors as the R demo (color-blind friendly)
site_colors = {"Bottomland": "#0072B2", "Upland": "#E69F00"}


#######################################################
###          2. LOAD AND LOOK AT THE DATA           ###
#######################################################
field = pd.read_csv("data/field_trial.csv")

print(field.head())                 # first 5 rows
print(field.shape)                  # (number of rows, number of columns)
print(field.isna().sum())           # counting missing values per column: yield has 3 missing values. read left to right.

# Remove the 3 plots with no yield
field_clean = field.dropna(subset=["yield_t_ha"]) # drop rows that contain NA values and look at yield_t_ha column to see what to drop.
print(field_clean.shape)            # 189 rows now (192 - 3 missing)


#######################################################
###     3. MATPLOTLIB: Histogram of yield ###
#######################################################
# matplotlib uses a FIGURE (the canvas) and AXES (the plot on it):
#     fig, ax = plt.subplots()
# Then you tell the axes exactly what to draw.


fig, ax = plt.subplots(figsize=(7, 4.5)) # create a figure and axes object.
ax.hist(field_clean["yield_t_ha"], bins=20, color="seagreen", edgecolor="black") # plot a histogram of the yield_t_ha column. split the yield range into 2.4 to 11.8 t/ha into 20 equal width bars.
ax.set_xlabel("Grain yield (t/ha)") # set the x-axis label.
ax.set_ylabel("Number of plots") # set the y-axis label.
ax.set_title("Distribution of maize yield") # set the title.
plt.show() # show the plot.


#######################################################
###    4. PANDAS: summarize first, then plot        ###
#######################################################
# Average yield for each nitrogen rate (same idea as group_by + summarise in R)
mean_yield = field_clean.groupby("nitrogen_kg_ha")["yield_t_ha"].mean() # group by nitrogen_kg_ha column and calculate the mean of the yield_t_ha column.
print(mean_yield) # print the mean yield for each nitrogen rate.

fig, ax = plt.subplots(figsize=(7, 4.5)) # create a figure and axes object.
ax.plot(mean_yield.index, mean_yield.values, marker="o", color="darkgreen") # plot a line plot of the mean yield for each nitrogen rate.
ax.set_xticks([0, 60, 120, 180]) # set the x-axis ticks.
ax.set_xlabel("Nitrogen rate (kg N/ha)") # set the x-axis label.
ax.set_ylabel("Mean grain yield (t/ha)") # set the y-axis label.
ax.set_title("Yield rises with nitrogen, then levels off") # set the title.
plt.show() # show the plot.


#######################################################
###  5. SEABORN: Boxplot of yield by nitrogen rate and site ###
#######################################################
# seaborn reads COLUMN NAMES straight from the table.
# hue="site" gives one color per site AND a legend, no extra code needed.

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=field_clean, x="nitrogen_kg_ha", y="yield_t_ha",
            hue="site", palette=site_colors, showfliers=False, ax=ax)
sns.stripplot(data=field_clean, x="nitrogen_kg_ha", y="yield_t_ha",
              hue="site", dodge=True, palette={"Bottomland": "black", "Upland": "black"},
              alpha=0.4, legend=False, ax=ax)           # black dots on top of the boxes
ax.set_xlabel("Nitrogen rate (kg N/ha)")
ax.set_ylabel("Grain yield (t/ha)")
ax.set_title("More nitrogen, more yield (gains shrink above 120 kg N/ha)")
ax.legend(title="Site")
plt.show()


#######################################################
###  6. SEABORN: Line plot of yield by nitrogen rate and site with confidence bands ###
#######################################################
# lineplot calculates the mean AND a 95% confidence interval for you.

fig, ax = plt.subplots(figsize=(7, 4.5)) # create a figure and axes object.
sns.lineplot(data=field_clean, x="nitrogen_kg_ha", y="yield_t_ha",
             hue="site", palette=site_colors, marker="o", ax=ax) # plot a line plot of the mean yield for each nitrogen rate and site.
ax.set_xticks([0, 60, 120, 180]) # set the x-axis ticks.
ax.set_xlabel("Nitrogen rate (kg N/ha)") # set the x-axis label.
ax.set_ylabel("Grain yield (t/ha)") # set the y-axis label.
ax.set_title("Average yield response to nitrogen") # set the title.
ax.legend(title="Site") # add a legend.
plt.show() # show the plot. add a confidence band around the line plot.


#######################################################
###   7. FACETS: Line plot of yield by nitrogen rate and site with confidence bands by year ###
#######################################################
# relplot(..., col="year") makes one panel per year (like facet_wrap in R)

g = sns.relplot(data=field_clean, x="nitrogen_kg_ha", y="yield_t_ha", # plot a line plot of the mean yield for each nitrogen rate and site.
                hue="site", palette=site_colors, col="year",
                kind="line", marker="o", height=4.5)
g.set_axis_labels("Nitrogen rate (kg N/ha)", "Grain yield (t/ha)")
g.set(xticks=[0, 60, 120, 180])
g.set_titles("{col_name}")              # panel titles "2024", "2025"
g.legend.set_title("Site")
g.figure.suptitle("The drier 2025 season gave lower yields at both sites", y=1.03)
plt.show()


#######################################################
###              8. SAVE THE FIGURE                 ###
#######################################################
# Saving in code means you can remake the exact same figure any time.
# PNG at 300 dpi for slides/posters; PDF for journals (stays sharp when zoomed).
g.savefig("figures/yield_by_nitrogen_python.png", dpi=300) # save the plot as a PNG file.
print("Saved! Look in the figures/ folder.")


#######################################################
###     OPTIONAL: an interactive plot (plotly)      ###
#######################################################
# Remove the # at the start of the 4 lines below to try it (needs: pip install plotly).
# It opens in your web browser: hover over a point to see which plot it came from.
#
# import plotly.express as px
# fig = px.scatter(field_clean, x="spad_chlorophyll", y="yield_t_ha", color="site",
#                  hover_data=["plot_id", "variety", "nitrogen_kg_ha"])
# fig.show()


#######################################################
###                    RECAP                        ###
#######################################################
# 1. pandas loads and summarizes the data; matplotlib and seaborn draw it.
# 2. matplotlib: total control, more code (fig, ax = plt.subplots()).
# 3. seaborn: less code, reads column names, hue= colors by group.
# 4. Always: labels WITH units, a title that states the finding, save in code.
#
#   Python (seaborn)              R (ggplot2)
#   hue="site"               ->   aes(color = site) / aes(fill = site)
#   col="year"               ->   facet_wrap(~ year)
#   g.savefig(...)           ->   ggsave(...)
#   df.groupby().mean()      ->   group_by() %>% summarise()