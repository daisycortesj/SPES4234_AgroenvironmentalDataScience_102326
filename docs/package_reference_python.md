# Python Package Reference 🐍

A field guide to tools you'll meet in papers, tutorials, and lab code. **You don't need these for class.** ✅ = used in today's lesson; 📚 = for later.

Every snippet below assumes you've run this first, from the repository's top folder:
```python
import pandas as pd
field = pd.read_csv("data/field_trial.csv")
```
Install anything with `pip install <name>` (or `%pip install <name>` inside a notebook).

---

## At a glance

| Package | Category | One-line summary | Plant-science use |
|---|---|---|---|
| ✅ **argparse** | Scripting (built in) | Command-line options for scripts | Run one plotting script on 50 sample files on a cluster |
| ✅ **numpy** | Math | Fast arrays and math | log-transform counts, compute indices like NDVI |
| ✅ **pandas** | Data tables | Read, filter, group, summarize DataFrames | Tidy field-trial or sensor data |
| ✅ **matplotlib** | Plotting: foundation | Full control of every element | Journal figures with exact panel sizes |
| ✅ **seaborn** | Plotting: statistical | One-line statistical plots from DataFrames | Box/strip plots of yield by treatment |
| 👀 **plotnine** | Plotting: grammar | ggplot2 syntax in Python | Share plotting code style with R users |
| 👀 **plotly** | Plotting: interactive | Hover/zoom plots, HTML export | Explore which plot an outlier came from |
| 📚 **joypy** | Plotting: specialty | Ridgeline ("joy") plots | Distribution of flowering time by genotype |
| 📚 **altair** (= **vega-altair**) | Plotting: grammar + interactive | Declarative, interactive charts | Linked, filterable views of trial data |
| 📚 **bokeh** | Plotting: interactive / web apps | Interactive browser plots and dashboards | A lab dashboard for greenhouse sensors |
| 📚 **hvPlot** | Plotting: interactive shortcut | Adds `.hvplot()` to pandas/polars/xarray | Quick interactive plots of big sensor time series |
| 📚 **polars** | Data tables | A very fast alternative to pandas | Large phenotyping or genomics tables |
| 📚 **optuna** | Machine learning | Automatic hyperparameter tuning (+ plots) | Tune a yield-prediction model |
| 📚 **shap** | Machine learning | Explain model predictions (+ plots) | Which weather/soil features drive predicted yield? |
| 📚 **MLflow** | Machine learning | Track experiments, parameters, figures | Keep a record of every model you trained |

> 📝 **Name notes:** "MLflor" in the original list is **MLflow**. **altair** and **vega-altair** are the *same* package: the project's name is Vega-Altair, you install it with `pip install altair`, and you `import altair as alt`.

---

## ✅ argparse (built into Python)
Not a plotting library. It makes a script accept options, so you don't edit code to change inputs. See [`python/argparse_example/quick_plot.py`](../python/argparse_example/quick_plot.py) and [`examples/python/volcano_cli.py`](../examples/python/volcano_cli.py).
```bash
python python/argparse_example/quick_plot.py -i data/field_trial.csv -x spad_chlorophyll -y yield_t_ha --hue site -o figures/spad.png
```
📖 [Official tutorial](https://docs.python.org/3/howto/argparse.html)

## ✅ numpy
The math engine underneath pandas, matplotlib, and most scientific Python.
```python
import numpy as np
log_yield = np.log2(field["yield_t_ha"] + 1)          # log transform
n_rates = np.arange(0, 181, 60)                        # 0, 60, 120, 180
```
📖 [numpy.org/doc](https://numpy.org/doc/stable/)

## ✅ pandas
Tables (DataFrames). `read_csv`, `head`, `info`, `describe`, `groupby`, `agg`, and `.plot()` for quick looks.
```python
field.groupby(["site", "nitrogen_kg_ha"])["yield_t_ha"].mean().unstack(0).plot(marker="o")
```
📖 [pandas.pydata.org/docs](https://pandas.pydata.org/docs/) · [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

## ✅ matplotlib
The foundation. Learn `fig, ax = plt.subplots()`, then `ax.plot / ax.scatter / ax.hist / ax.set(...)`. For exact layouts, `plt.axes([left, bottom, width, height])` places panels by hand (see `examples/python/`).
```python
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(8, 3))
axes[0].hist(field["yield_t_ha"].dropna(), bins=20)
axes[1].scatter(field["spad_chlorophyll"], field["yield_t_ha"], alpha=0.5)
fig.tight_layout()
```
📖 [matplotlib.org](https://matplotlib.org/stable/) · [Cheatsheets](https://matplotlib.org/cheatsheets/)

## ✅ seaborn
Statistical plots in one line, straight from a DataFrame: `hue=` (color by group), `col=`/`row=` (facets).
```python
import seaborn as sns
sns.catplot(data=field, x="nitrogen_kg_ha", y="yield_t_ha", hue="variety", col="site", kind="box")
```
📖 [seaborn.pydata.org](https://seaborn.pydata.org/) · [Example gallery](https://seaborn.pydata.org/examples/index.html)

---

## 👀 plotnine
The grammar of graphics (ggplot2) in Python. Code moves almost line-for-line between R and Python. Note the quotes around column names and the outer parentheses.
```python
from plotnine import ggplot, aes, geom_boxplot, facet_wrap, labs, theme_bw
plot = (ggplot(field.dropna(subset=["yield_t_ha"]), aes("factor(nitrogen_kg_ha)", "yield_t_ha", fill="site"))
        + geom_boxplot()
        + facet_wrap("~year")
        + labs(x="N rate (kg/ha)", y="Yield (t/ha)")
        + theme_bw())
plot.save("figures/plotnine_box.png", dpi=300, width=7, height=3.5)
```
📖 [plotnine.org](https://plotnine.org/)

## 👀 plotly
Interactive plots: hover for details, zoom, click legend entries to hide groups. Save as an HTML file to share.
```python
import plotly.express as px
fig = px.scatter(field, x="spad_chlorophyll", y="yield_t_ha", color="site",
                 facet_col="year", hover_data=["plot_id", "variety"])
fig.write_html("figures/interactive_scatter.html")
```
📖 [plotly.com/python](https://plotly.com/python/)

---

## 📚 joypy
Ridgeline plots: stacked, overlapping density curves. Great for comparing many distributions at once.
```python
import joypy
fig, axes = joypy.joyplot(field.dropna(subset=["yield_t_ha"]), by="nitrogen_kg_ha",
                          column="yield_t_ha", figsize=(5, 4), colormap=plt.cm.YlGn)
```
⚠️ **Heads-up:** joypy is updated rarely. In testing (October 2026), joypy 0.2.6 worked with pandas 2.x but **failed with pandas 3.0** (`TypeError: 'generator' object is not subscriptable`). If you hit this, use a separate environment with `pip install "pandas<3" joypy`, or use seaborn's [ridge plot recipe](https://seaborn.pydata.org/examples/kde_ridgeplot.html), which does the same thing with tools you already have.

📖 [github.com/leotac/joypy](https://github.com/leotac/joypy) · R equivalent: `ggridges`

## 📚 altair (Vega-Altair)
Declarative grammar (like ggplot2) that outputs **interactive** web charts. Strong at linked views (select in one chart, filter another).
```python
import altair as alt
chart = alt.Chart(field.dropna()).mark_circle().encode(
    x=alt.X("spad_chlorophyll", title="SPAD", scale=alt.Scale(zero=False)),
    y=alt.Y("yield_t_ha", title="Yield (t/ha)"),
    color="site",
    tooltip=["plot_id", "variety", "nitrogen_kg_ha"],
).interactive()
chart.save("figures/altair_scatter.html")
```
📖 [altair-viz.github.io](https://altair-viz.github.io/)

## 📚 bokeh
Interactive plots and small web apps/dashboards in the browser. More code than plotly, more control.
```python
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
source = ColumnDataSource(field.dropna())
p = figure(x_axis_label="SPAD", y_axis_label="Yield (t/ha)",
           tools="pan,wheel_zoom,reset,hover", tooltips=[("plot", "@plot_id"), ("variety", "@variety")])
p.scatter("spad_chlorophyll", "yield_t_ha", source=source, alpha=0.6)
output_file("figures/bokeh_scatter.html")
save(p)
```
📖 [docs.bokeh.org](https://docs.bokeh.org/)

## 📚 hvPlot
Adds a `.hvplot` method to pandas (and polars, xarray…) for one-line interactive plots (built on HoloViews + Bokeh). Handy for large time series.
```python
import hvplot.pandas  # noqa: F401  (this import adds .hvplot to DataFrames)
plot = field.hvplot.scatter(x="spad_chlorophyll", y="yield_t_ha", by="site", hover_cols=["plot_id"])
hvplot.save(plot, "figures/hvplot_scatter.html")
```
📖 [hvplot.holoviz.org](https://hvplot.holoviz.org/)

## 📚 polars
A fast DataFrame library (an alternative to pandas), useful when tables get big (millions of rows). Different syntax: expressions with `pl.col()`. Install with `pip install polars pyarrow` (`pyarrow` is needed for `.to_pandas()`).
```python
import polars as pl
pf = pl.read_csv("data/field_trial.csv")
summary = (pf.group_by("site", "nitrogen_kg_ha")
             .agg(pl.col("yield_t_ha").mean().alias("mean_yield"))
             .sort("site", "nitrogen_kg_ha"))
print(summary)
sns.lineplot(data=summary.to_pandas(), x="nitrogen_kg_ha", y="mean_yield", hue="site")  # hand off to seaborn
```
📖 [docs.pola.rs](https://docs.pola.rs/)

---

## 📚 Machine-learning tools that *make* plots
These aren't plotting libraries, but they produce figures you'll see in ML papers.

### optuna: hyperparameter tuning
Tries many model settings automatically. `optuna.visualization` draws (plotly) charts of the search.
```python
import optuna
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

data = field.dropna()
X = data[["nitrogen_kg_ha", "soil_moisture_pct", "spad_chlorophyll", "plant_height_cm"]]
y = data["yield_t_ha"]

def objective(trial):
    model = RandomForestRegressor(n_estimators=trial.suggest_int("n_estimators", 20, 200),
                                  max_depth=trial.suggest_int("max_depth", 2, 10), random_state=0)
    return cross_val_score(model, X, y, cv=3, scoring="r2").mean()

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=15)
optuna.visualization.plot_optimization_history(study).write_html("figures/optuna_history.html")
```
📖 [optuna.org](https://optuna.org/)

### shap: explaining model predictions
Shows how much each input pushed a prediction up or down. The **beeswarm** plot is common in ag/environmental ML papers.
```python
import shap
model = RandomForestRegressor(n_estimators=100, random_state=0).fit(X, y)
shap_values = shap.Explainer(model, X)(X)
shap.plots.beeswarm(shap_values, show=False)
plt.savefig("figures/shap_beeswarm.png", dpi=300, bbox_inches="tight")
```
📖 [shap.readthedocs.io](https://shap.readthedocs.io/)

### MLflow: experiment tracking
A lab notebook for models: logs parameters, metrics, and **figures** for every run, browsable in a local web UI (`mlflow ui`).
```python
import mlflow
with mlflow.start_run(run_name="rf_yield"):
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("r2", 0.71)
    mlflow.log_artifact("figures/shap_beeswarm.png")   # attach a figure to this run
# then in a terminal:  mlflow ui   → open http://127.0.0.1:5000
```
📖 [mlflow.org/docs](https://mlflow.org/docs/latest/index.html)

---

## Which should I learn next?
1. **Get comfortable with pandas + seaborn + matplotlib.** They cover 90% of figures.
2. Need **interactive**? → plotly (easiest) → altair or bokeh.
3. Collaborate with **R users**? → plotnine.
4. Data too **big** for pandas? → polars.
5. Doing **ML**? → shap for interpretation, optuna for tuning, MLflow for record-keeping.

*Written October 2026. Packages change, so if a link breaks, search for the package name plus "documentation".*
