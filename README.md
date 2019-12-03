# Python + Chart.js = plots
Used JS and CSS scripts (from www.chartjs.org) for rendering a cute plots in Jupyter Notebook

Example of usage in demo.ipynb (demo.html)

```python
from chart_js import cjs_plot
```


```python
cjs_line = cjs_plot()
cjs_line.add_dataset('line', 'x1', [1, 2, 3, 4, 11, 2, 12], [1, 2, 3, 4])
cjs_line.add_dataset('line', 'x2', [5, 6, 10, 8, 3, 12], [1, 2, 3, 4, 5, 6])
cjs_line.add_options('Line plot', 'x-value', 'y-value',display_legend=True, size=(3, 6))
cjs_line.render(['x1', 'x2'],'Line plot')
```

![Image description](https://github.com/romatolmach/python_chart_js_plot/blob/master/screenshot.png)
