# Examples from past projects

| File | What it shows | Run from the repo's top folder |
|---|---|---|
| [`python/volcano_cli.py`](python/volcano_cli.py) | A volcano plot built "by hand": numpy + matplotlib + **argparseAdapted from BME163 Week 3. | `python examples/python/volcano_cli.py -i data/de_results.csv -o figures/volcano_cli.png` 
| [`python/marginal_histograms_two_ways.py`](python/marginal_histograms_two_ways.py) | The **same figure two ways**: ~40 lines of low-level matplotlib (`Rectangle` patches, manual panels) vs. **one** `sns.jointplot` call. | `python examples/python/marginal_histograms_two_ways.py` |

💡 Try `volcano_cli.py` with different thresholds to see why argparse is handy:
```bash
python examples/python/volcano_cli.py -i data/de_results.csv -o figures/volcano_strict.png --fc 2 --padj 1e-10
```

### Why look at low-level matplotlib at all?
Seaborn and ggplot2 are faster for everyday work. But when a journal demands a figure **exactly 3.42 inches wide** with panels in precise positions, or you need a plot type no library offers, the BME163 approach (`plt.axes([left, bottom, width, height])`, drawing shapes yourself) gives total control. Compare the two outputs of `marginal_histograms_two_ways.py` to see the trade-off.
