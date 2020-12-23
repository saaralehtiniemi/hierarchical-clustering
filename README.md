# Hierarchical Clustering
Clustering software for performing agglomerative hierarchical clustering. 
Compares the performance of different linkage and affinity metrics with several cluster numbers. 
Visualizes cluster hierarchies as dendrograms and real-vs-predicted cluster labels as confusion matrixes.

## Create virtual environment and install requirements
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
## Run scripts
See the `--help` option of the main script
```
source venv/bin/activate
python3 src/main.py --help
```

### PARAMETERS
The script uses the parameters:
```
file					(REQUIRED) The dataset used for the clustering
--output				(OPTIONAL) The folder the results will be placed, by default "results"
--class_column		(OPTIONAL) If desired, you can specify the column in the file which is used as class labels
```

The `file` doesn't need to contain a header. So the data could look like, for example (The iris dataset, from https://archive.ics.uci.edu/ml/datasets/Iris):

| sepal_length | sepal_width | petal_length | petal_width | species |
| --- | --- | --- | --- | --- |
| 5.1 | 3.5 | 1.4 | 0.2 | setosa |
| 4.9 | 3.0 | 1.4 | 0.2 | setosa |
| 4.7 | 3.2 | 1.3 | 0.2 | setosa |
| 4.6 | 3.1 | 1.5 | 0.2 | setosa |
| 5.0 | 3.6 | 1.4 | 0.2 | setosa |
...
Or
| --- | --- | --- | --- | --- |
| 5.1 | 3.5 | 1.4 | 0.2 | setosa |
| 4.9 | 3.0 | 1.4 | 0.2 | setosa |
| 4.7 | 3.2 | 1.3 | 0.2 | setosa |
| 4.6 | 3.1 | 1.5 | 0.2 | setosa |
| 5.0 | 3.6 | 1.4 | 0.2 | setosa |
...

It should be noted that only the numerical data is used in the clustering, so columns with text-data will be dropped. Also, rows with `Nan`-values will be dropped.

If a column give by the  `class_column` is not found in the data, the script will not use any class labels. The `class_column` can contain either labels or encoded numerically. If the column contains text-labels, they will be visible in the images too.

You can give multiple datafiles and class labels at the same time. 

### USAGE
Here are some examples of usage:

One dataset named `data.csv`, no labels.
```
python3 -u main.py data.csv
```
One dataset named `data.csv`, labels in column named `A`.
```
python3 -u main.py data.csv --class_column A
```
Two datasets named `data1.csv` and `data2.csv`, no labels.
```
python3 -u main.py data1.csv,data2.csv
```
Two datasets named `data1.csv` and `data2.csv`, labels in column named `A`.
```
python3 -u main.py data1.csv,data2.csv --class_column A
```
Two datasets named `data1.csv` and `data2.csv`, labels in column named `A` and `B` (`A` for `data1.csv` and `B` for `data2.csv`).
```
python3 -u main.py data1.csv,data2.csv --class_column A,B
```