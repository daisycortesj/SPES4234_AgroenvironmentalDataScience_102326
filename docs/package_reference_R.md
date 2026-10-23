# R Package Reference 📊

A field guide to the R tools you'll meet in papers, tutorials, and lab code. **You don't need these for class.** ✅ = used in today's lesson; 👀 = shown briefly; 📚 = for later.

Every snippet assumes you opened `SPES4234_AgroenvironmentalDataScience_102326.Rproj` and ran:
```r
library(ggplot2)
library(dplyr)
field  <- read.csv("data/field_trial.csv")
growth <- read.csv("data/growth_curves.csv")
de     <- read.csv("data/de_results.csv")
```

**How to install:** most packages come from **CRAN**: `install.packages("name")`. Packages marked **🧬 Bioconductor** install differently:
```r
install.packages("BiocManager")         # once
BiocManager::install("EnhancedVolcano") # then any Bioconductor package
```

---

## At a glance

| Package | Where | Category | One-line summary |
|---|---|---|---|
| ✅ **ggplot2** | CRAN | Plotting core | Grammar of graphics: build plots in layers |
| ✅ **dplyr** | CRAN | Data wrangling | `filter`, `mutate`, `group_by`, `summarise` |
| ✅ **tidyr** | CRAN | Data wrangling | Reshape: `pivot_longer`, `pivot_wider` |
| 👀 **ggraph** | CRAN | Networks | ggplot2-style network and tree plots |
| 👀 **ggdist** | CRAN | Distributions | Raincloud, half-eye, interval plots; great for uncertainty |
| 📚 **patchwork** | CRAN | Layout | Combine plots with `+` and `/` into multi-panel figures |
| 📚 **ggpubr** | CRAN | Publication helpers | Ready-made plots + p-value brackets |
| 📚 **ggrepel** | CRAN | Labels | Labels that don't overlap |
| 📚 **ggbeeswarm** | CRAN | Raw data | Beeswarm points (non-overlapping jitter) |
| 📚 **ggstatsplot** | CRAN | Stats + plot | Plot with the statistical test printed on it |
| 📚 **pheatmap** | CRAN | Heatmaps | Clustered heatmaps in one line |
| 📚 **ComplexHeatmap** | 🧬 Bioconductor | Heatmaps | Highly customizable heatmaps with annotations |
| 📚 **EnhancedVolcano** | 🧬 Bioconductor | Genomics | Publication volcano plots |
| 📚 **edgeR** | 🧬 Bioconductor | Genomics (analysis) | RNA-seq differential expression (+ MDS/BCV plots) |
| 📚 **clusterProfiler** | 🧬 Bioconductor | Genomics (analysis) | GO/KEGG enrichment (+ dot plots) |
| 📚 **gganimate** | CRAN | Animation | Turn a ggplot into a GIF/video |
| 📚 **ggalluvial** | CRAN | Flows | Alluvial/Sankey-style plots of category changes |
| 📚 **ggforce** | CRAN | Extensions | Annotate groups, zoom facets, and more |
| 📚 **ggfx** | CRAN | Effects | Shadows, glows, blurs on layers |
| 📚 **circlize** | CRAN | Circular plots | Circos/chord diagrams (genomes, relationships) |
| 📚 **ggstream** | CRAN | Time series | Streamgraphs |
| 📚 **ggpattern** | CRAN | Fills | Pattern fills (stripes, dots) for B&W printing |
| 📚 **brms** | CRAN | Models | Bayesian mixed models (uses Stan) |
| 📚 **glmmTMB** | CRAN | Models | Fast generalized linear mixed models |
| 📚 **mgcv** | CRAN (comes with R) | Models | GAMs: smooth, nonlinear trends |
| 📚 **targets** | CRAN | Workflow | Reproducible pipelines; `tar_visnetwork()` draws the pipeline |

> 📝 **Name note:** "gggraph" in the original list is **ggraph** (two g's).
> 📝 **Category note:** edgeR, clusterProfiler, brms, glmmTMB, mgcv, and targets are **analysis/workflow** packages, not plotting packages, but each produces figures you'll see in plant science papers, so they're here.

---

## ✅ Core: ggplot2 · dplyr · tidyr
```r
field %>%                                              # take the data, and then...
  filter(year == 2025) %>%                             # keep 2025 only
  group_by(site, nitrogen_kg_ha) %>%                   # group
  summarise(mean_yield = mean(yield_t_ha, na.rm = TRUE), .groups = "drop") %>%
  ggplot(aes(nitrogen_kg_ha, mean_yield, color = site)) +
  geom_line() + geom_point() +
  labs(x = "N rate (kg/ha)", y = "Mean yield (t/ha)")

# tidyr: wide <-> long. Long format = one row per measurement (ggplot2 loves this)
long <- tidyr::pivot_longer(field, cols = c(yield_t_ha, plant_height_cm),
                            names_to = "trait", values_to = "value")
```
📖 [ggplot2](https://ggplot2.tidyverse.org/) · [dplyr](https://dplyr.tidyverse.org/) · [tidyr](https://tidyr.tidyverse.org/) · [Posit cheatsheets](https://posit.co/resources/cheatsheets/) · [*R for Data Science*](https://r4ds.hadley.nz/)

## 👀 ggraph: networks and trees
Correlation networks, co-expression networks, phylogeny-like trees. Works with `igraph`/`tidygraph` objects. Full example in [`R/01_demo.R`](../R/01_demo.R) §8.
📖 [ggraph.data-imaginist.com](https://ggraph.data-imaginist.com/)

## 👀 ggdist: distributions and uncertainty
Raincloud plots (density + box + raw points), and plots of model uncertainty (e.g., from brms). Full raincloud example in [`R/01_demo.R`](../R/01_demo.R) §8.
```r
library(ggdist)
ggplot(field, aes(x = yield_t_ha, y = variety)) +
  stat_halfeye()          # density + median + intervals
```
📖 [mjskay.github.io/ggdist](https://mjskay.github.io/ggdist/)

---

## 📚 Layout & publication helpers

### patchwork: combine plots
```r
library(patchwork)
p1 <- ggplot(field, aes(yield_t_ha)) + geom_histogram(bins = 20)
p2 <- ggplot(field, aes(spad_chlorophyll, yield_t_ha)) + geom_point()
p3 <- ggplot(field, aes(factor(nitrogen_kg_ha), yield_t_ha)) + geom_boxplot()
(p1 | p2) / p3 + plot_annotation(tag_levels = "A")   # A, B, C panel labels
```
📖 [patchwork.data-imaginist.com](https://patchwork.data-imaginist.com/)

### ggpubr: quick publication plots + p-values
```r
library(ggpubr)
field$N <- factor(field$nitrogen_kg_ha)
ggboxplot(field, x = "N", y = "yield_t_ha", add = "jitter", fill = "N") +
  stat_compare_means(method = "anova")
```
📖 [rpkgs.datanovia.com/ggpubr](https://rpkgs.datanovia.com/ggpubr/)

### ggrepel: labels that don't overlap
```r
library(ggrepel)
top <- de %>% slice_min(padj, n = 10)
ggplot(de, aes(log2FoldChange, -log10(padj))) +
  geom_point(color = "gray60", size = 0.8) +
  geom_text_repel(data = top, aes(label = gene), max.overlaps = Inf)
```
📖 [ggrepel.slowkow.com](https://ggrepel.slowkow.com/)

### ggbeeswarm: show every point without overlap
```r
library(ggbeeswarm)
ggplot(field, aes(factor(nitrogen_kg_ha), yield_t_ha, color = site)) +
  geom_quasirandom(dodge.width = 0.7)
```
📖 [github.com/eclarke/ggbeeswarm](https://github.com/eclarke/ggbeeswarm)

### ggstatsplot: the statistical test, printed on the plot
Runs the test for you (here, comparing sites) and adds the statistics as a subtitle. Read up on the default test choices before using it in a paper.
```r
library(ggstatsplot)
ggbetweenstats(data = field, x = site, y = yield_t_ha)
```
📖 [indrajeetpatil.github.io/ggstatsplot](https://indrajeetpatil.github.io/ggstatsplot/)

---

## 📚 Heatmaps

Shared setup: a matrix of trait means, with rows = traits and columns = variety × N.
```r
mat <- field %>%
  group_by(variety, nitrogen_kg_ha) %>%
  summarise(across(c(yield_t_ha, spad_chlorophyll, plant_height_cm, grain_protein_pct, days_to_flowering),
                   ~ mean(.x, na.rm = TRUE)), .groups = "drop") %>%
  mutate(id = paste(variety, nitrogen_kg_ha, sep = "_N")) %>%
  select(-variety, -nitrogen_kg_ha) %>%
  tibble::column_to_rownames("id") %>%
  as.matrix() %>% t()
```

### pheatmap: clustered heatmap in one line
```r
library(pheatmap)
pheatmap(mat, scale = "row", cluster_cols = TRUE, main = "Trait means (row z-scores)")
```
📖 [CRAN: pheatmap](https://cran.r-project.org/package=pheatmap)

### ComplexHeatmap 🧬: everything customizable
```r
library(ComplexHeatmap)
z <- t(scale(t(mat)))                                       # row z-scores
top_ann <- HeatmapAnnotation(N = sub(".*_N", "", colnames(mat)))
Heatmap(z, name = "z-score", top_annotation = top_ann)
```
📖 [ComplexHeatmap Complete Reference (free book)](https://jokergoo.github.io/ComplexHeatmap-reference/book/)

---

## 📚 Genomics (Bioconductor 🧬)

### EnhancedVolcano: publication volcano plots
```r
library(EnhancedVolcano)
EnhancedVolcano(de, lab = de$gene, x = "log2FoldChange", y = "padj",
                pCutoff = 0.05, FCcutoff = 1, title = "Drought vs control (simulated)")
```
📖 [Bioconductor: EnhancedVolcano](https://bioconductor.org/packages/EnhancedVolcano/)

### edgeR: RNA-seq differential expression
Works on a **count matrix** (genes × samples), not on the results table. Its plots (MDS, BCV, MD) check data quality before testing.
```r
library(edgeR)
set.seed(1)
counts <- matrix(rnbinom(6000, mu = 50, size = 5), ncol = 6,
                 dimnames = list(NULL, paste0(rep(c("ctrl", "drought"), each = 3), 1:3)))
group <- factor(rep(c("control", "drought"), each = 3))
y <- DGEList(counts, group = group)
y <- calcNormFactors(y)
plotMDS(y, col = as.numeric(group))       # do samples cluster by treatment?
```
📖 [Bioconductor: edgeR](https://bioconductor.org/packages/edgeR/) · the edgeR User's Guide is excellent

### clusterProfiler: GO / KEGG enrichment
Needs **real gene IDs** and an annotation package for your species (e.g., `org.At.tair.db` for *Arabidopsis*), so it won't run on the simulated data.
```r
# library(clusterProfiler); library(org.At.tair.db)
# ego <- enrichGO(gene = my_sig_tair_ids, OrgDb = org.At.tair.db, keyType = "TAIR", ont = "BP")
# dotplot(ego, showCategory = 15)
```
📖 [Biomedical Knowledge Mining using GOSemSim and clusterProfiler (free book)](https://yulab-smu.top/biomedical-knowledge-mining-book/)

---

## 📚 Special plot types

### gganimate: animated plots
Needs a renderer: install `gifski` too.
```r
library(gganimate)
anim <- ggplot(growth, aes(days_after_planting, height_cm, group = plot_id, color = factor(nitrogen_kg_ha))) +
  geom_line() +
  labs(color = "N rate", x = "Days after planting", y = "Height (cm)") +
  transition_reveal(days_after_planting)
# animate(anim, renderer = gifski_renderer("figures/growth.gif"))
```
📖 [gganimate.com](https://gganimate.com/)

### ggalluvial: how categories change
Example: did plots stay in the same yield class from 2024 to 2025?
```r
library(ggalluvial)
classes <- field %>%
  mutate(yield_class = cut(yield_t_ha, c(0, 6, 9, Inf), labels = c("Low", "Mid", "High")),
         unit = paste(site, block, variety, nitrogen_kg_ha)) %>%
  select(unit, year, yield_class) %>%
  tidyr::pivot_wider(names_from = year, values_from = yield_class, names_prefix = "y") %>%
  count(y2024, y2025) %>% filter(!is.na(y2024), !is.na(y2025))
ggplot(classes, aes(axis1 = y2024, axis2 = y2025, y = n)) +
  geom_alluvium(aes(fill = y2024)) + geom_stratum() +
  geom_text(stat = "stratum", aes(label = after_stat(stratum))) +
  scale_x_discrete(limits = c("2024", "2025")) + labs(y = "Number of plots", fill = "2024 class")
```
📖 [corybrunson.github.io/ggalluvial](https://corybrunson.github.io/ggalluvial/)

### ggforce: annotate groups and zoom
```r
library(ggforce)
ggplot(field, aes(soil_moisture_pct, yield_t_ha, color = site)) +
  geom_point() +
  geom_mark_ellipse(aes(fill = site, label = site), alpha = 0.1)
```
📖 [ggforce.data-imaginist.com](https://ggforce.data-imaginist.com/)

### ggfx: shadows, glows, blur
Use sparingly in scientific figures. Good for posters and highlighting one layer.
```r
library(ggfx)
ggplot(field, aes(spad_chlorophyll, yield_t_ha)) +
  geom_point(color = "gray80") +
  with_shadow(geom_smooth(method = "lm", color = "darkgreen"), sigma = 3)
```
📖 [ggfx.data-imaginist.com](https://ggfx.data-imaginist.com/)

### circlize: circular plots
Circos plots of genomes (chromosomes around a circle) and chord diagrams of relationships.
```r
library(circlize)
m <- with(field, tapply(yield_t_ha, list(variety, nitrogen_kg_ha), mean, na.rm = TRUE))
colnames(m) <- paste0("N", colnames(m))
chordDiagram(m)
circos.clear()
```
📖 [Circular Visualization in R (free book)](https://jokergoo.github.io/circlize_book/book/)

### ggstream: streamgraphs
```r
library(ggstream)
growth %>% group_by(days_after_planting, variety) %>%
  summarise(height = mean(height_cm), .groups = "drop") %>%
  ggplot(aes(days_after_planting, height, fill = variety)) +
  geom_stream(type = "ridge")
```
📖 [github.com/davidsjoberg/ggstream](https://github.com/davidsjoberg/ggstream)

### ggpattern: stripes and dots instead of (or with) color
Useful when figures will be printed in black & white.
```r
library(ggpattern)
field %>% group_by(site, variety) %>% summarise(y = mean(yield_t_ha, na.rm = TRUE), .groups = "drop") %>%
  ggplot(aes(variety, y, pattern = site)) +
  geom_col_pattern(position = "dodge", fill = "white", color = "black", pattern_fill = "black") +
  labs(y = "Mean yield (t/ha)")
```
📖 [coolbutuseless.github.io/package/ggpattern](https://coolbutuseless.github.io/package/ggpattern/)

---

## 📚 Statistical models that make figures

Field trials have **blocks, years, and sites**, so mixed models (random effects) are the norm. These packages fit the model; their plots show the fitted effects.

### glmmTMB: fast mixed models
```r
library(glmmTMB)
field$N <- factor(field$nitrogen_kg_ha)
fit <- glmmTMB(yield_t_ha ~ N * site + (1 | year:block), data = field)
summary(fit)
newdat <- expand.grid(N = levels(field$N), site = unique(field$site))
newdat$pred <- predict(fit, newdata = newdat, re.form = NA)   # population-level predictions
ggplot(newdat, aes(N, pred, color = site, group = site)) + geom_line() + geom_point() +
  labs(x = "N rate (kg/ha)", y = "Predicted yield (t/ha)")
```
📖 [glmmTMB on CRAN](https://cran.r-project.org/package=glmmTMB) · Tip: the `ggeffects` or `emmeans` packages make prediction plots easier

### mgcv: smooth curves (GAMs)
Fits flexible curves without picking a formula, e.g., growth over the season.
```r
library(mgcv)
growth$N <- factor(growth$nitrogen_kg_ha)
gam_fit <- gam(height_cm ~ N + s(days_after_planting, by = N), data = growth)
plot(gam_fit, pages = 1, shade = TRUE)    # one smooth per N rate
```
📖 [mgcv on CRAN](https://cran.r-project.org/package=mgcv) · Gavin Simpson's `gratia` package draws mgcv results with ggplot2

### brms: Bayesian mixed models
Same formula style as glmmTMB, fitted with Stan. ⚠️ Needs a **C++ compiler** (Rtools on Windows; Xcode Command Line Tools on Mac). Install and test well before you need it. Pairs beautifully with **ggdist**.
```r
# library(brms)
# fit_b <- brm(yield_t_ha ~ N * site + (1 | year:block), data = field, cores = 4)
# plot(conditional_effects(fit_b), ask = FALSE)
```
📖 [paul-buerkner.github.io/brms](https://paul-buerkner.github.io/brms/)

---

## 📚 Workflow: targets + `tar_visnetwork()`
`targets` turns your analysis into a pipeline that re-runs only what changed. `tar_visnetwork()` draws the pipeline as an interactive graph (needs the `visNetwork` package). Put this in a file named `_targets.R` in the project folder:
```r
# _targets.R
library(targets)
tar_option_set(packages = c("ggplot2", "dplyr"))
list(
  tar_target(raw_file, "data/field_trial.csv", format = "file"),
  tar_target(field, read.csv(raw_file)),
  tar_target(summary_tbl, field |> group_by(nitrogen_kg_ha) |> summarise(y = mean(yield_t_ha, na.rm = TRUE))),
  tar_target(fig, ggsave("figures/pipeline_plot.png",
                         ggplot(summary_tbl, aes(nitrogen_kg_ha, y)) + geom_line(), width = 4, height = 3),
             format = "file")
)
```
Then in the console: `targets::tar_visnetwork()` to see the graph, and `targets::tar_make()` to run it.
📖 [The {targets} R package user manual](https://books.ropensci.org/targets/)

---

## Which should I learn next?
1. **ggplot2 + dplyr + tidyr** until they feel natural. They are the foundation for nearly everything above.
2. Making **multi-panel figures**? → patchwork.
3. Doing **RNA-seq**? → edgeR (or DESeq2) → EnhancedVolcano → clusterProfiler; ComplexHeatmap for expression heatmaps.
4. Analyzing **field trials**? → glmmTMB (or lme4) + emmeans/ggeffects; later brms + ggdist.
5. Analysis getting **long and messy**? → targets.

*Written October 2026. Packages change, so if a link breaks, search for the package name plus "documentation".*
