# Final Understanding Check ✅

Four minutes. **Questions 1–4:** vote by show of hands (about 30 seconds each). **Question 5:** write it on your exit ticket and hand it in on the way out.

---

**1. You want the mean yield for each nitrogen rate. Which tool does that job?**
- A) matplotlib (Python) / ggplot2 (R)
- B) pandas (Python) / dplyr (R)
- C) argparse (Python) / ggdist (R)
- D) seaborn (Python) / ggraph (R)

**2. In ggplot2, what does the code inside `aes()` do?**
- A) Sets the colors of the plot background
- B) Maps columns in your data to visual properties (x, y, color, size…)
- C) Saves the plot to a file
- D) Loads the data

**3. Your plot has a y-axis labeled `yield_t_ha` and a legend titled `nitrogen_kg_ha`. What's the best fix?**
- A) Nothing; the column names are accurate
- B) Rename to "Grain yield (t/ha)" and "Nitrogen rate (kg N/ha)"
- C) Remove the axis label and legend to reduce clutter
- D) Make the font bigger

**4. What is `argparse` used for?**
- A) Making interactive plots
- B) Reading Excel files
- C) Letting a Python script accept options from the command line (e.g., `-i input.csv -o figure.png`)
- D) Choosing color palettes

---

### ✍️ Exit ticket (write and hand in)

**5.** What would you change to make this figure ready for a paper? List **two** things.
```python
plt.scatter(df["soil_moisture_pct"], df["yield_t_ha"])
plt.show()
```

**Bonus (optional):** What's one figure from your own research you'd like to remake in code?

---

### 🏠 Extra practice (after class, optional)

**6.** Which line is the seaborn equivalent of ggplot2's `color = site` inside `aes()`?
A) `color="site"` passed to `plt.figure()` · B) `hue="site"` · C) `col="site"` · D) `palette="site"`

**7.** You have yield for 4 hybrids at 2 sites and want readers to compare the sites without clutter. Which approach fits best?
A) A pie chart for each hybrid · B) Facets: one panel per site · C) A 3D bar chart · D) One histogram of all 192 values

**8.** Name one Python and one R plotting tool from today, and write one sentence on when you'd use each.
