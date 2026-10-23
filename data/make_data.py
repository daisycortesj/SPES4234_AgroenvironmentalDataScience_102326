"""
make_data.py — creates the SIMULATED datasets used in this workshop.

Nothing in these files is real experimental data. The numbers are generated
with known patterns (more nitrogen -> more yield, up to a plateau; the
Bottomland site is wetter; etc.) so that the plots have something to "find".

Run from the repository root:
    python data/make_data.py

You do NOT need to run this for the workshop — the CSV files are already here.
It is included so you can see how the data were made (reproducibility!).
"""

import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(seed=163)  # fixed seed = same data every time
out_dir = Path(__file__).parent

# ---------------------------------------------------------------------------
# 1. field_trial.csv — a maize nitrogen x variety trial, 2 sites, 2 years
# ---------------------------------------------------------------------------
years = [2024, 2025]
sites = {"Upland": {"moisture": 18, "yield_bonus": 0.0},
         "Bottomland": {"moisture": 27, "yield_bonus": 0.8}}
varieties = {"Hybrid_A": 0.0, "Hybrid_B": 0.6, "Hybrid_C": -0.4, "Hybrid_D": 0.3}
n_rates = [0, 60, 120, 180]          # kg N per hectare
blocks = [1, 2, 3]

rows = []
plot_counter = 0
for year in years:
    year_effect = 0.0 if year == 2024 else -0.7   # 2025 = drier year
    for site, s in sites.items():
        for block in blocks:
            for variety, v_eff in varieties.items():
                for n in n_rates:
                    plot_counter += 1
                    # yield responds to N with diminishing returns (plateau)
                    n_response = 5.5 * (1 - np.exp(-n / 70))
                    soil_moisture = rng.normal(s["moisture"] + (-3 if year == 2025 else 0), 2.5)
                    yield_t_ha = (4.5 + n_response + v_eff + s["yield_bonus"]
                                  + year_effect + 0.05 * (soil_moisture - 20)
                                  + rng.normal(0, 0.6))
                    spad = 38 + 12 * (1 - np.exp(-n / 60)) + rng.normal(0, 2.2)
                    height = 185 + 0.18 * n + 8 * v_eff + rng.normal(0, 9)
                    flowering = int(round(68 - 0.015 * n + 2 * (variety == "Hybrid_C")
                                          + rng.normal(0, 1.5)))
                    protein = 7.5 + 0.012 * n + rng.normal(0, 0.45)
                    rows.append({
                        "plot_id": f"P{plot_counter:03d}",
                        "year": year,
                        "site": site,
                        "block": block,
                        "variety": variety,
                        "nitrogen_kg_ha": n,
                        "soil_moisture_pct": round(soil_moisture, 1),
                        "spad_chlorophyll": round(spad, 1),
                        "plant_height_cm": round(height, 1),
                        "days_to_flowering": flowering,
                        "grain_protein_pct": round(protein, 2),
                        "yield_t_ha": round(max(yield_t_ha, 0.5), 2),
                    })

field = pd.DataFrame(rows)
# a few realistic missing values (a plot lost to deer, a broken SPAD meter...)
missing_idx = rng.choice(field.index, size=6, replace=False)
field.loc[missing_idx[:3], "yield_t_ha"] = np.nan
field.loc[missing_idx[3:], "spad_chlorophyll"] = np.nan
field.to_csv(out_dir / "field_trial.csv", index=False)

# ---------------------------------------------------------------------------
# 2. growth_curves.csv — weekly plant height for a subset of plots (2025)
# ---------------------------------------------------------------------------
growth_rows = []
subset = field[(field.year == 2025) & (field.block == 1)]
for _, plot in subset.iterrows():
    final_h = plot["plant_height_cm"]
    k = 0.11 + 0.0002 * plot["nitrogen_kg_ha"]          # growth rate
    midpoint = 52 - 0.02 * plot["nitrogen_kg_ha"]        # days to half height
    for dap in range(14, 99, 7):                          # days after planting
        h = final_h / (1 + np.exp(-k * (dap - midpoint))) + rng.normal(0, 3)
        growth_rows.append({
            "plot_id": plot["plot_id"],
            "site": plot["site"],
            "variety": plot["variety"],
            "nitrogen_kg_ha": plot["nitrogen_kg_ha"],
            "days_after_planting": dap,
            "height_cm": round(max(h, 2), 1),
        })
pd.DataFrame(growth_rows).to_csv(out_dir / "growth_curves.csv", index=False)

# ---------------------------------------------------------------------------
# 3. de_results.csv — simulated differential expression (drought vs control)
#    For the BONUS volcano plot. Gene symbols borrowed from well-known
#    Arabidopsis drought-response genes so labels look familiar; the
#    statistics are invented.
# ---------------------------------------------------------------------------
n_genes = 3000
log2fc = rng.normal(0, 0.9, n_genes)
pvals = 10 ** -np.abs(rng.normal(0, 1.2, n_genes))
# make ~120 genes truly changed
idx = rng.choice(n_genes, 120, replace=False)
log2fc[idx] = rng.choice([-1, 1], 120) * rng.uniform(1.5, 6, 120)
pvals[idx] = 10 ** -rng.uniform(4, 40, 120)
pvals = np.clip(pvals, 1e-300, 1)

gene_ids = [f"Gene_{i:05d}" for i in range(1, n_genes + 1)]
famous_up = ["RD29A", "RD29B", "RAB18", "NCED3", "DREB2A", "LEA14", "ERD10", "COR15A", "P5CS1", "ABF3"]
famous_down = ["CAB1", "RBCS1A", "LHCB3", "EXPA1", "PIF4"]
# give the famous names to the most significant up- and down-regulated genes
by_signif = np.argsort(pvals)
top_up = [i for i in by_signif if log2fc[i] > 1][:len(famous_up)]
top_down = [i for i in by_signif if log2fc[i] < -1][:len(famous_down)]
for i, name in zip(top_up, famous_up):
    gene_ids[i] = name
for i, name in zip(top_down, famous_down):
    gene_ids[i] = name

# Benjamini-Hochberg adjusted p-values
order = np.argsort(pvals)
ranked = pvals[order] * n_genes / (np.arange(n_genes) + 1)
ranked = np.minimum.accumulate(ranked[::-1])[::-1]
padj = np.empty(n_genes)
padj[order] = np.clip(ranked, 0, 1)

de = pd.DataFrame({
    "gene": gene_ids,
    "baseMean": np.round(10 ** rng.uniform(0.5, 4, n_genes), 1),
    "log2FoldChange": np.round(log2fc, 3),
    "pvalue": pvals,
    "padj": padj,
})
de.to_csv(out_dir / "de_results.csv", index=False)

print("Wrote:", ", ".join(p.name for p in sorted(out_dir.glob("*.csv"))))
print("field_trial:", field.shape, "| growth_curves:", len(growth_rows), "rows | de_results:", de.shape)
