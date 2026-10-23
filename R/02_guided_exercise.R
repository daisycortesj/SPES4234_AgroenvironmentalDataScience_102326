#######################################################
###   02 · GUIDED EXERCISE (R) — ~10 minutes        ###
#######################################################
# Question: Does more nitrogen make leaves greener (higher SPAD chlorophyll),
#           and does that depend on the variety?
#
# HOW THIS WORKS
# * Work with a neighbor. 
# * Replace every ___ (three underscores) with the right code, then run it.
# * Hints are in the comments. Answers: R/solutions/02_guided_exercise_SOLUTION.R
# * Error "unexpected input" (pointing at ___) just means a blank is still empty.
# * Run ONE step at a time (select the lines, then Ctrl+Enter). Don't click "Source" — the empty
#   blanks would stop the whole file.

library(ggplot2)
library(dplyr)

#######################################################
### Step 1 · Load the data
#######################################################
# HINT: the file is data/field_trial.csv (open the .Rproj so this path works)
field <- read.csv("___")
head(field)

#######################################################
### Step 2 · Check for missing values
#######################################################
# HINT: is.na() marks missing cells TRUE; colSums() counts the TRUEs per column
colSums(___(field))

#######################################################
### Step 3 · Summarize with dplyr
#######################################################
# Mean SPAD for every combination of variety and nitrogen rate.
# HINT: group_by() takes BOTH grouping columns separated by a comma.
#       na.rm = TRUE tells mean() to skip missing values.
spad_summary <- field %>%
  group_by(variety, ___) %>%
  summarise(mean_spad = mean(___, na.rm = TRUE), .groups = "drop")
spad_summary

#######################################################
### Step 4 · First draft plot
#######################################################
# Nitrogen on x, mean SPAD on y, one colored line per variety.
# HINT: inside aes(), use column names WITHOUT quotes. Use spad_summary as data.
ggplot(spad_summary, aes(x = ___, y = ___, color = ___)) +
  geom_line() +
  geom_point()

#######################################################
### Step 5 · Polish it and save it
#######################################################
# Needs: axis labels WITH units, a title that states the finding, a nice theme.
# Then save it IN CODE so you can remake it any time.
# HINT: labs(title = "...", x = "...", y = "...", color = "...")
#       ggsave(file, plot, width, height, dpi)  — 300 dpi is a good default
p_spad <- ggplot(spad_summary, aes(x = nitrogen_kg_ha, y = mean_spad, color = variety)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  scale_x_continuous(breaks = c(0, 60, 120, ___)) +
  labs(title = "___",
       x = "___",
       y = "___",
       color = "Variety") +
  theme_classic()
p_spad
ggsave("figures/spad_by_variety.png", p_spad, width = 6, height = 4, dpi = ___)

#######################################################
### Step 6 · Answer the question (write it as a comment!)
#######################################################
# In ONE sentence: Does more nitrogen make leaves greener, and does it depend on variety?
# ANSWER:


#######################################################
###  BONUS 
#######################################################
# Does the pattern hold at both sites? One panel per site.
# HINT: this time we plot the RAW data (every plot) and let stat_summary draw the mean line.
#       facet_wrap(~ column_name) makes one panel per group.
p_sites <- field %>%
  filter(!is.na(spad_chlorophyll)) %>%          # drop the 3 plots with no SPAD reading
  ggplot(aes(x = nitrogen_kg_ha, y = spad_chlorophyll, color = variety)) +
  geom_point(alpha = 0.3) +
  stat_summary(fun = mean, geom = "line", linewidth = 1) +
  facet_wrap(~ ___) +
  labs(x = "Nitrogen rate (kg N/ha)", y = "SPAD chlorophyll", color = "Variety") +
  theme_bw()
p_sites
ggsave("figures/spad_by_site.png", p_sites, width = 7, height = 3.5, dpi = 300)