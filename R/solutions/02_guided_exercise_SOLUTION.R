#######################################################
###   02 · GUIDED EXERCISE (R) — SOLUTION           ###
#######################################################
library(ggplot2)
library(dplyr)

### Step 1 · Load the data
field <- read.csv("data/field_trial.csv")
head(field)

### Step 2 · Check for missing values
colSums(is.na(field))      # 3 missing yields, 3 missing SPAD readings

### Step 3 · Summarize with dplyr
spad_summary <- field %>%
  group_by(variety, nitrogen_kg_ha) %>%
  summarise(mean_spad = mean(spad_chlorophyll, na.rm = TRUE), .groups = "drop")
spad_summary

# Bonus: a wide table that is easier to read (tidyr)
tidyr::pivot_wider(spad_summary, names_from = nitrogen_kg_ha, values_from = mean_spad)

### Step 4 · First draft plot
ggplot(spad_summary, aes(x = nitrogen_kg_ha, y = mean_spad, color = variety)) +
  geom_line() +
  geom_point()

### Step 5 · Polish it and save it
p_spad <- ggplot(spad_summary, aes(x = nitrogen_kg_ha, y = mean_spad, color = variety)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  scale_x_continuous(breaks = c(0, 60, 120, 180)) +
  labs(title = "Leaf greenness rises with N, then levels off",
       x = "Nitrogen rate (kg N/ha)",
       y = "Mean SPAD chlorophyll (unitless)",
       color = "Variety") +
  theme_classic()
p_spad
ggsave("figures/spad_by_variety.png", p_spad, width = 6, height = 4, dpi = 300)

### Step 6 · Answer
# SPAD chlorophyll increases with nitrogen and plateaus above ~120 kg N/ha; all four
# hybrids follow nearly the same curve, so the response does NOT appear to depend on
# variety. (A formal test would use a mixed model, e.g. glmmTMB or lme4.)

### BONUS · Facets: same pattern at both sites
p_sites <- ggplot(field, aes(x = nitrogen_kg_ha, y = spad_chlorophyll, color = variety)) +
  geom_point(alpha = 0.3) +
  stat_summary(fun = mean, geom = "line", linewidth = 1) +
  facet_wrap(~ site) +
  labs(x = "Nitrogen rate (kg N/ha)", y = "SPAD chlorophyll", color = "Variety") +
  theme_bw()
p_sites
ggsave("figures/spad_by_site.png", p_sites, width = 7, height = 3.5, dpi = 300)
