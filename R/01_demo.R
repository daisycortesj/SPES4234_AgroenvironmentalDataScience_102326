#######################################################
###   01 · LIVE DEMO — Plotting a Field Trial in R   ###
#######################################################
# Question: Does nitrogen fertilizer increase maize yield,
#           and is the response the same at both sites?
#
# Data: data/field_trial.csv (SIMULATED maize trial, 192 plots)
#
# HOW TO RUN: open the .Rproj file first (so R can find the data), then put
# your cursor on a line and press:
#   Cmd + Return (Mac)   or   Ctrl + Enter (Windows)
#
# Lines starting with # are COMMENTS: notes for humans. R ignores them.


#######################################################
###              1. LOAD THE PACKAGES                ###
#######################################################
# install.packages("ggplot2")  # only needed ONCE per computer
library(ggplot2)   # makes the plots
library(dplyr)     # prepares the data (like pandas in Python)


#######################################################
###          2. LOAD AND LOOK AT THE DATA            ###
#######################################################
field <- read.csv("data/field_trial.csv")

head(field)                  # first 6 rows
dim(field)                   # number of rows, number of columns
summary(field$yield_t_ha)    # quick stats for yield. Notice "NA's: 3"

# 3 plots have no yield (missing values = NA). We remove them, and tell R to
# treat nitrogen and year as CATEGORIES (groups) instead of plain numbers.
field_clean <- field %>%                       # %>% means "and then"
  filter(!is.na(yield_t_ha)) %>%               # keep rows where yield is NOT missing
  mutate(nitrogen = factor(nitrogen_kg_ha),    # 0, 60, 120, 180 become 4 groups
         year     = factor(year))

dim(field_clean)             # 189 rows now (192 - 3 missing)


#######################################################
###       3. BUILD ONE PLOT, ONE LAYER AT A TIME     ###
#######################################################
# A ggplot is built in LAYERS joined with "+":
#   data + aes() (which column goes where)  ->  geom (what shape)  ->  labels & style

# 3a. The empty canvas: R knows the data and the axes, but not what to draw yet
ggplot(field_clean, aes(x = nitrogen, y = yield_t_ha))

# 3b. Add a layer: one box per nitrogen rate
ggplot(field_clean, aes(x = nitrogen, y = yield_t_ha)) +
  geom_boxplot()

# 3c. Add another layer: every plot as a dot (show the raw data, not just a summary)
ggplot(field_clean, aes(x = nitrogen, y = yield_t_ha)) +
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(width = 0.15, alpha = 0.5)

# 3d. Ask a bigger question: is it the same at both sites?
#     Map site to fill color INSIDE aes() -> one color per site, plus a legend
ggplot(field_clean, aes(x = nitrogen, y = yield_t_ha, fill = site)) +
  geom_boxplot(outlier.shape = NA) +
  geom_point(position = position_jitterdodge(jitter.width = 0.15, seed = 1),
             alpha = 0.4)

# 3e. Make it a figure someone else can read:
#     color-blind-friendly colors, labels WITH units, a title that states the finding
p_yield <- ggplot(field_clean, aes(x = nitrogen, y = yield_t_ha, fill = site)) +
  geom_boxplot(outlier.shape = NA) +
  geom_point(position = position_jitterdodge(jitter.width = 0.15, seed = 1),
             alpha = 0.4) +
  scale_fill_manual(values = c(Bottomland = "#0072B2", Upland = "#E69F00")) +
  labs(title = "More nitrogen, more yield (gains shrink above 120 kg N/ha)",
       x = "Nitrogen rate (kg N/ha)",
       y = "Grain yield (t/ha)",
       fill = "Site") +
  theme_classic(base_size = 14)

p_yield      # typing the name of a saved plot shows it


#######################################################
###     4. FACETS: one panel per year, in one line   ###
#######################################################
p_final <- p_yield + facet_wrap(~ year)
p_final
# The drier 2025 season gave lower yields at both sites.


#######################################################
###        5. dplyr: SUMMARIZE FIRST, THEN PLOT      ###
#######################################################
# Same question, different view: the AVERAGE yield at each nitrogen rate.
yield_means <- field_clean %>%
  group_by(site, nitrogen_kg_ha) %>%               # one group per site x N rate
  summarise(mean_yield = mean(yield_t_ha),
            se         = sd(yield_t_ha) / sqrt(n()),   # standard error
            .groups    = "drop")

yield_means      # a small table: 2 sites x 4 nitrogen rates = 8 rows

ggplot(yield_means, aes(x = nitrogen_kg_ha, y = mean_yield, color = site)) +
  geom_line(linewidth = 1) +
  geom_point(size = 3) +
  geom_errorbar(aes(ymin = mean_yield - se, ymax = mean_yield + se), width = 6) +
  scale_x_continuous(breaks = c(0, 60, 120, 180)) +
  scale_color_manual(values = c(Bottomland = "#0072B2", Upland = "#E69F00")) +
  labs(title = "Average yield response to nitrogen",
       x = "Nitrogen rate (kg N/ha)",
       y = "Mean grain yield (t/ha), +/- SE",
       color = "Site") +
  theme_classic(base_size = 14)


#######################################################
###               6. SAVE THE FIGURE                 ###
#######################################################
# Saving in code means you can remake the exact same figure any time.
ggsave("figures/yield_by_nitrogen_R.png", p_final, width = 9, height = 4.5, dpi = 300)
# Look in the figures/ folder (Files pane, bottom right) to see it!


#######################################################
###                     RECAP                        ###
#######################################################
# 1. ggplot builds a plot in LAYERS joined by +   (data + aes -> geom -> labs -> theme)
# 2. Put a column INSIDE aes() to map it to color/fill  ->  you get a legend for free
# 3. dplyr (%>%, filter, mutate, group_by, summarise) prepares data BEFORE plotting
# 4. facet_wrap() makes one panel per group; ggsave() saves at a set size and dpi
#
#   Python (seaborn)          R (ggplot2)
#   hue="site"           ->   aes(color = site) / aes(fill = site)
#   col="year"           ->   facet_wrap(~ year)
#   fig.savefig(...)     ->   ggsave(...)
#   df.groupby().mean()  ->   group_by() %>% summarise()