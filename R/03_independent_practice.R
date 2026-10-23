#######################################################
###  03 · INDEPENDENT PRACTICE (R) — ~7 minutes     ###
#######################################################
# IN CLASS, try Challenge A. At Home, try Challenge B, C, and D.
# No blanks this time — you write the code.
# Copy and adapt code from 01_demo.R and 02_guided_exercise.R.
#
#  A ----- Growth curves over the season ------   data/growth_curves.csv (in class)
#  B ----- Heatmap of yield by variety x N ------  data/field_trial.csv(in class)
#  C ----- Fix the ugly plot -------------------- data/field_trial.csv(take-home)
#  D ----- Bonus: volcano plot ------------------ data/de_results.csv(take-home)
#
# Solutions: R/solutions/03_independent_practice_SOLUTION.R

library(ggplot2)
library(dplyr)

#######################################################
### Challenge A -  Growth curves
#######################################################
# Question: How does plant height change over the season, and does nitrogen change it?
# 1. Average the height for each day and N rate:
#      group_by(days_after_planting, nitrogen_kg_ha) %>% summarise(mean_height = mean(height_cm))
# 2. Plot it: x = days_after_planting, y = mean_height, color = factor(nitrogen_kg_ha)
#      + geom_line() + geom_point()
# 3. Add labels with units with labs(), and save with ggsave()
growth <- read.csv("data/growth_curves.csv")
head(growth)

# your code here


#######################################################
### Challenge B - Heatmap 
#######################################################
# Question: Which variety x nitrogen combination gave the highest average yield?
# 1. group_by(variety, nitrogen_kg_ha) %>% summarise(mean_yield = mean(yield_t_ha, na.rm = TRUE))
# 2. ggplot(..., aes(x = factor(nitrogen_kg_ha), y = variety, fill = mean_yield)) + geom_tile()
# 3. Add the numbers: geom_text(aes(label = round(mean_yield, 1)))
# 4. Nice colors: scale_fill_distiller(palette = "YlGn", direction = 1)
field <- read.csv("data/field_trial.csv")

# your code here

#######################################################
### Challenge C - Fix the ugly plot
#######################################################
# Problems with the ugly plot:
# 1. Two different things (yield AND height / 20!) share one y-axis -> confusing.
# 2. No axis labels, no units, and the title "data" says nothing.
# 3. Big solid dots pile on top of each other (overplotting).
# 4. No legend: what do red and orange mean?
# 5. It ignores site, which probably explains the pattern.
#
# The fix: ONE variable per plot, color by site, see-through dots, clear labels.

# Step 1: remove the 3 plots with no yield (avoids the "Removed 3 rows" warning)
field_yield <- field %>%
  filter(!is.na(yield_t_ha))

# Step 2: plot only yield (one variable), colored by site
# Step 3: see-through dots (alpha) so overlapping points stay visible
# Step 4: clear labels WITH units and a title that states the finding
p_fixed <- ggplot(field_yield, aes(x = soil_moisture_pct, y = yield_t_ha, color = site)) +
  geom_point(size = 2.5, alpha = 0.6) +
  scale_color_manual(values = c(Bottomland = "#0072B2", Upland = "#E69F00")) +
  labs(title = "Wetter Bottomland plots tended to yield more",
       x = "Soil moisture (%)",
       y = "Grain yield (t/ha)",
       color = "Site") +
  theme_classic(base_size = 14)

# Step 5: show it and save it
print(p_fixed)
ggsave("figures/moisture_fixed_R.png", p_fixed, width = 7, height = 4.5, dpi = 300)



#######################################################
### Challenge D - Bonus: volcano plot 
#######################################################
# Question: Which genes change the most under drought? (simulated RNA-seq results)
# * x = log2FoldChange, y = -log10(padj)
# * Make a column with mutate(): significant = padj < 0.05 & abs(log2FoldChange) > 1
# * color = significant; scale_color_manual(values = c("gray70", "firebrick"))
# * Stretch: label the top 10 genes with ggrepel::geom_text_repel() (if installed)
# * Even more stretch: try EnhancedVolcano (Bioconductor) — see docs/package_reference_R.md
de <- read.csv("data/de_results.csv")

# your code here

