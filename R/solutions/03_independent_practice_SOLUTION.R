#######################################################
###  03 · INDEPENDENT PRACTICE (R) — SOLUTIONS      ###
#######################################################
# Example solutions. There are many correct answers in data visualization!
library(ggplot2)
library(dplyr)

field <- read.csv("data/field_trial.csv")

#######################################################
### Challenge A · Growth curves
#######################################################
growth <- read.csv("data/growth_curves.csv")

# Step 1: average height for each day and nitrogen rate
growth_means <- growth %>%
  group_by(days_after_planting, nitrogen_kg_ha) %>%
  summarise(mean_height = mean(height_cm), .groups = "drop")

# Step 2: one line per nitrogen rate
p_growth <- ggplot(growth_means, aes(x = days_after_planting, y = mean_height,
                                     color = factor(nitrogen_kg_ha))) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  scale_color_viridis_d(end = 0.9) +        # color-blind-friendly colors
  labs(title = "More nitrogen, taller plants",
       x = "Days after planting",
       y = "Mean plant height (cm)",
       color = "N rate (kg/ha)") +
  theme_classic(base_size = 14)
p_growth
ggsave("figures/growth_curves_R.png", p_growth, width = 7, height = 4.5, dpi = 300)

#######################################################
### Challenge B · Heatmap
#######################################################
# Step 1: average yield for each variety and nitrogen rate (16 combinations)
yield_tbl <- field %>%
  group_by(variety, nitrogen_kg_ha) %>%
  summarise(mean_yield = mean(yield_t_ha, na.rm = TRUE), .groups = "drop")
yield_tbl          # check: 16 rows

# Step 2: one colored tile per combination, with the number written on it
p_heat <- ggplot(yield_tbl, aes(x = factor(nitrogen_kg_ha), y = variety, fill = mean_yield)) +
  geom_tile(color = "white") +                        # the colored squares
  geom_text(aes(label = round(mean_yield, 1)), size = 5) +   # the numbers
  scale_fill_distiller(palette = "YlGn", direction = 1) +    # light = low, dark green = high
  labs(title = "Mean yield by variety and nitrogen rate",
       x = "Nitrogen rate (kg N/ha)",
       y = "Variety",
       fill = "Yield (t/ha)") +
  theme_minimal(base_size = 14)
p_heat             # this line SHOWS the plot
ggsave("figures/yield_heatmap_R.png", p_heat, width = 7, height = 4, dpi = 300)

#######################################################
### Challenge C · Fix the ugly plot
#######################################################
# Problems:
# 1. Two different variables (yield and height / 20!) share one unlabeled y-axis.
# 2. No axis labels or units; the title "data" says nothing.
# 3. Big solid points overlap (overplotting); no legend explains red vs orange.
# 4. Ignores the obvious grouping (site) that likely explains the pattern.
#
# Fix: reshape to long format with tidyr, one variable per panel, color by site.
library(tidyr)
long <- field %>%
  select(plot_id, site, soil_moisture_pct, yield_t_ha, plant_height_cm) %>%
  pivot_longer(c(yield_t_ha, plant_height_cm), names_to = "trait", values_to = "value") %>%
  mutate(trait = recode(trait, yield_t_ha = "Grain yield (t/ha)",
                               plant_height_cm = "Plant height (cm)"))

p_fixed <- ggplot(long, aes(x = soil_moisture_pct, y = value, color = site)) +
  geom_point(alpha = 0.6, size = 1.8) +
  facet_wrap(~ trait, scales = "free_y") +      # each panel gets its own y-axis
  labs(title = "Wetter Bottomland plots tended to yield more",
       x = "Soil moisture (%)", y = NULL, color = "Site") +
  theme_bw()
p_fixed
ggsave("figures/moisture_fixed_R.png", p_fixed, width = 8, height = 3.5, dpi = 300)

#######################################################
### Challenge D · Volcano plot
#######################################################
# A volcano plot shows ALL genes at once:
#   x = how much a gene changed (log2 fold change): left = DOWN, right = UP in drought
#   y = how confident we are (-log10 adjusted p-value): higher = more significant
library(ggrepel)   # keeps gene labels from overlapping. Install once: install.packages("ggrepel")

# Step 1: load the data and look at it
de <- read.csv("data/de_results.csv")
head(de)

# Step 2: add two new columns
#   neg_log10_padj = the y-axis value (small p-values become BIG numbers)
#   result         = "Significant" if padj < 0.05 AND the gene changed more than 2-fold
de <- de %>%
  mutate(neg_log10_padj = -log10(padj),
         result = ifelse(padj < 0.05 & abs(log2FoldChange) > 1,
                         "Significant", "Not significant"))
table(de$result)    # how many genes in each group?

# Step 3: pick the 10 most significant genes to label
top_genes <- de %>%
  slice_min(padj, n = 10)

# Step 4: build the plot
p_volcano <- ggplot(de, aes(x = log2FoldChange, y = neg_log10_padj, color = result)) +
  geom_point(size = 1.5, alpha = 0.6) +                                    # every gene
  geom_hline(yintercept = -log10(0.05), linetype = "dashed") +             # p = 0.05 cutoff
  geom_vline(xintercept = c(-1, 1), linetype = "dashed") +                 # 2-fold change cutoffs
  geom_text_repel(data = top_genes, aes(label = gene), color = "black", size = 3.5) +  # labels
  scale_color_manual(values = c("Not significant" = "gray70", "Significant" = "firebrick")) +
  labs(title = "Drought-responsive genes (simulated)",
       x = "log2 fold change (drought vs control)",
       y = "-log10 adjusted p-value",
       color = NULL) +
  theme_classic(base_size = 14)

# Step 5: show it and save it
print(p_volcano)
ggsave("figures/volcano_R.png", p_volcano, width = 7, height = 5.5, dpi = 300)