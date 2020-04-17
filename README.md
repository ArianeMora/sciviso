# sciviso
[![codecov.io](https://codecov.io/github/ArianeMora/sciviso/coverage.svg?branch=master)](https://codecov.io/github/ArianeMora/sciviso?branch=master)
[![PyPI](https://img.shields.io/pypi/v/sciviso)](https://pypi.org/project/sciviso/)

## A wrapper to format all plots the same 

Shared functions:

```
# Builds the plot
chart.plot()

# Saves to svg
chart.save_svg([directory, filename])

# Saves to png
chart.save_png([directory, filename], dpi=100)

# Returns svg string 
chart.get_svg()
```

## Barchart

Standard seaborn wrapper. See documentation.
```
barchart = Barchart(df: pd.DataFrame, x: object, y: object, title='', xlabel='', ylabel='', hue=None, order=None,
                 hue_order=None)
```

## Boxplot
Wrapper to create a box plot with option for annotating statistics.

```
boxplot = Boxplot(df: pd.DataFrame, x: object, y: object, title='', xlabel='', ylabel='', 
                    hue=None, order=None, hue_order=None)

# Also you can use the boxplot class to format data for the boxplot from a standard dataframe
boxplot.format_data_for_boxplot(df: pd.DataFrame, conditions: list, filter_column=None, filter_values=None):

# Here we create a new dataframe with the columns: Conditions, Samples, Values
"""
Conditions: for each of the conditions that the user specified we check if that is in a c
olumn of the dataframe, if it is then that column's values are added to values and labelled with that condition
Samples: original name of the column
Values: value from that column for each row

e.g. df.columns = 'gender,      control_s1,     control_s2,     drug_1,     drug_2'
     df.values = [['female',    12              11              9           8],
                  ['male',      10              19              5           4]]
I could format it to a boxplot with conditions=['control', 'drug'], filter_column='gender', ['female']

"""
```

## Heatmap

Wrapper on seaborns clustermap. See that for details.
```
heatmap = Heatmap(df: pd.DataFrame, chart_columns: list, row_index: str, title='', xlabel='', ylabel='',
                 cluster_rows=True, cluster_cols=True, row_colours=None, vmin=None, vmax=None)


```
## Scatterplot
Scatter with optional annotation & regression (toDo.)
```
scatter = Scatterplot(self, df: pd.DataFrame, x: object, y: object, title='', xlabel='', ylabel='', colour=None,
                 points_to_annotate=None, annotation_label=None, add_correlation=False, correlation='Spearman')
```

## Violinplot
Very similar to the box plot just without the stats annotation. You can use the boxplot formatter to format the data
for the violin plot.

```
violinplot = Violinplot(self, df: pd.DataFrame, x: object, y: object, title='', xlabel='', ylabel='', hue=None, order=None,
                 hue_order=None, showfliers=False, add_dots=False)
```

## Volcanoplot
Volcano plot with annotation of selected values or all the top values.

```
volcano = Volcanoplot(self, df: pd.DataFrame, log_fc: str, p_val: str, label_column: str, title='',
                 xlabel='', ylabel='', invert=False, p_val_cutoff=0.05,
                 log_fc_cuttoff=2, label_big_sig=False, colours=None, offset=0, values_to_label=None)
```