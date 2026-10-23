# Introduction to Data Visualization using python + R

## Goal
You'll make the same kinds of plots in **Python** and **R** using one (simulated) maize field trial, and leave with a map of the plotting tools you'll meet in papers, tutorials, and lab code.

> **New to coding?** We will go through the code but you will mostly *run and edit* code. Copying, pasting, and changing things is how everyone learns. Eventually, you can use these examples as a guide for your work in the future or use for practice. 

---

# Start here

You'll use the **same Python setup you already use in this course**, plus RStudio if you follow the R scripts.

### 1. Open a terminal
- **Mac:** open **Terminal** (Cmd + Space → type "Terminal").
- **Windows:** open **Git Bash** or **Anaconda Prompt** from the Start menu.

### 2. Go to the folder where you keep your class work
For example:
```bash
cd ~/Documents
```

### 3. Clone the repository
```bash
git clone https://github.com/daisycortesj/SPES4234_AgroenvironmentalDataScience_102326.git
```
This creates a folder called `SPES4234_AgroenvironmentalDataScience_102326` containing all the workshop files.

### 4. Move into the folder
```bash
cd SPES4234_AgroenvironmentalDataScience_102326
```

### 5. Run the live demo (pick ONE option)

**Option A: Use your usual Python (most people, recommended for today)**
From this folder, in the same terminal:
```bash
python3 python/01_demo.py
```
On Windows with Anaconda, use `python` instead of `python3`. Each plot opens in its own window. Close the window to continue to the next plot.

**Option B (optional): Create a separate environment for this workshop**
An *environment* is a separate "box" with its own Python and packages, so this workshop can't interfere with your other projects. The file `environment.yml` is the shopping list of what goes in the box. Requires Anaconda/conda.
```bash
conda env create -f environment.yml    # build the box (once; takes a few minutes)
conda activate spes4234-dataviz        # step into the box (each time you work)
python python/01_demo.py               # run the demo using what's in the box
```
When you're done: `conda deactivate`.

### 6. Edit the scripts in an editor
Open the `.py` files in the editor you already use for this class (VS Code, Cursor, or a plain text editor). Save, then re-run the command above. For the R half, double-click `SPES4234_AgroenvironmentalDataScience_102326.Rproj` and run lines in RStudio with **Cmd + Return** (Mac) or **Ctrl + Enter** (Windows).

**What you'll do in class**

| Part | Python (hands-on, everyone) | R (instructor demo) |
|---|---|---|
| 1 · Live demo | `python/01_demo.py` | Watch on screen · `R/01_demo.R` |
| 2 · Guided exercise | `python/02_guided_exercise.py` | Optional if you have RStudio: `R/02_guided_exercise.R` |
| 3 · Independent practice | `python/03_independent_practice.py` | Optional: `R/03_independent_practice.R` |
| Solutions | `python/solutions/` | `R/solutions/` |


---

## By the end of this session you will be able to:

1. **Describe** the main plotting tools in Python (matplotlib, seaborn, pandas, and friends) and R (ggplot2 + dplyr and friends) and when you'd choose each.
2. **Load, inspect, and summarize** a table of field data before plotting it.
3. **Build** a histogram, scatter plot, line plot of means, and faceted plot in Python, and read the equivalent ggplot2 code in R.
4. **Improve** a draft figure so it stands alone: a question-driven title, axis labels with units, a readable legend, accessible colors.
5. **Save** a figure at publication quality from code. Solutions are in the `solutions/` folders.


---

## Tools Used

### Python 

| Tool | Role 
|---|---|---|
| **`numpy`** | Fast math on arrays (means, logs, sequences) 
| **`pandas`** | Opens data tables,filter rows, calculate summaries  
| **`matplotlib`** | The foundation of Python plotting (axes, colors, labels)
| **`seaborn`** | Makes common plots (scatter, box, line with error bars)
| **`argparse`** | NOT A PLOTTING TOOL. Lets you run a script with different settings without editing 
| `plotnine` · `plotly` | Like ggplot2 in R but in Python · interactive plots 
| `joypy` · `altair` · `bokeh` · `hvPlot` · `polars` · `optuna` · `shap` · `MLflow` | Specialty tools |  [reference](docs/package_reference_python.md) |

### R 

| Tool | Role 
|---|---|---|
| **`ggplot2`** | R's main plotting tool. Build a plot in **layers** joined with `+`: first the data, then the shape (points, lines, bars), then labels and style. 
| **`dplyr`** | Prepares tables with simple action words: `filter` (keep some rows), `group_by` + `summarise` (averages per group), `mutate` (add a column). Similar to pandas.
| **`tidyr`** | Reshapes tables, switching between "wide" (one column per measurement) and "long" (one row per measurement). ggplot2 prefers long.  
| `ggdist`, `ggraph`,`patchwork`, `ggpubr`, `ggrepel`, `pheatmap`, `ComplexHeatmap`, `EnhancedVolcano`, `edgeR`, `clusterProfiler`, `gganimate`, `brms`, `glmmTMB`, `mgcv`, `targets`, and more | Specialty tools | [reference](docs/package_reference_R.md) |

---

##  What's in this repository

```
SPES4234_AgroenvironmentalDataScience_102326/
├── README.md                         ← you are here
├── SPES4234_AgroenvironmentalDataScience_102326.Rproj   ← double-click to open the R project in RStudio
├── requirements.txt                  ← Python packages (pip)
├── environment.yml                   ← Python packages (conda)
├── data/
│   ├── field_trial.csv               ← main dataset (simulated maize N trial, 192 plots)
│   ├── growth_curves.csv             ← weekly plant height (for practice)
│   ├── de_results.csv                ← simulated RNA-seq results (bonus volcano plot)
│   ├── make_data.py                  ← how the data were simulated
│   └── README.md                     ← data dictionary (what every column means)
├── python/
│   ├── 01_demo.py                    ← live demo (run from the terminal)
│   ├── 02_guided_exercise.py         ← fill-in-the-blank exercise
│   ├── 03_independent_practice.py    ← write the plots yourself
│   ├── argparse_example/
│   │   └── quick_plot.py             ← plotting from the command line
│   └── solutions/
│       ├── 02_guided_exercise_SOLUTION.py
│       └── 03_independent_practice_SOLUTION.py
├── R/
│   ├── 00_install_packages.R         ← install ggplot2, dplyr, and friends (once)
│   ├── 01_demo.R                     ← same demo, in RStudio
│   ├── 02_guided_exercise.R
│   ├── 03_independent_practice.R
│   └── solutions/
│       ├── 02_guided_exercise_SOLUTION.R
│       └── 03_independent_practice_SOLUTION.R
├── examples/                         ← past projects: low-level matplotlib, volcano plots
│   ├── README.md
│   └── python/
│       ├── marginal_histograms_two_ways.py
│       └── volcano_cli.py
├── figures/                          ← saved plots go here
└── docs/
    ├── understanding_check.md        ← end-of-class questions
    ├── git_basics.md
    ├── package_reference_python.md
    └── package_reference_R.md
```


##  Further learning

* [*Practical Computing for Biologists*](https://practicalcomputing.org/) — Steven H. D. Haddock & Casey W. Dunn; [example files and quick reference](https://practicalcomputing.org/downloads.html)
* Lesson structure inspired by The Carpentries' teaching practices: [carpentries.org](https://carpentries.org)
* [*Fundamentals of Data Visualization*](https://clauswilke.com/dataviz/) — Claus O. Wilke (free online)
* [*R for Data Science* (2e)](https://r4ds.hadley.nz/) — Wickham, Çetinkaya-Rundel & Grolemund (free online)
* [*Python Data Science Handbook*](https://jakevdp.github.io/PythonDataScienceHandbook/) — Jake VanderPlas (free online)
* [From Data to Viz](https://www.data-to-viz.com/) — pick the right chart for your data
