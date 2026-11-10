# -*- coding: utf-8 -*-
"""Data science and ML course, part 1: workflow, NumPy, pandas, Matplotlib, data prep, regression."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "What data science is, and the tools",
 ("Data science", [
  "Data science | turns | Data into decisions",
  "Workflow | starts with | A question",
  "Pandas | handles | Tables",
  "NumPy | handles | Arrays",
  "Matplotlib | draws | Plots",
  "Scikit-learn | builds | Models",
  "Keras | builds | Neural networks"]),
 ["Data science is the practice of asking questions of data and answering them with statistics, programming and judgement. Machine learning is the part where a program learns a pattern from examples instead of being given rules.",
  "A typical project follows a loop: ask a question, collect data, clean it, explore it, build a model, evaluate it honestly, and communicate. Most of the time goes into data, not models.",
  "Python's toolkit is layered. NumPy gives fast arrays, pandas gives tables, Matplotlib draws charts, scikit-learn gives classic machine learning, and Keras gives neural networks."],
 [("Machine learning", "Methods in which a program improves at a task by learning patterns from data."),
  ("Feature", "An input variable used to make a prediction, such as age or price."),
  ("Label (target)", "The value we want to predict."),
  ("Supervised learning", "Learning from examples that include the correct answer (regression and classification)."),
  ("Unsupervised learning", "Finding structure in data without labels, such as clusters.")],
 ["Question, data, clean, explore, model, evaluate, communicate.",
  "Supervised: features X and labels y.",
  "Regression predicts numbers; classification predicts categories.",
  "Unsupervised: clustering, dimension reduction.",
  "The tools: NumPy, pandas, Matplotlib, scikit-learn, Keras."],
 [T("A shop owner wonders which customers will return next month. A doctor wants to spot a disease early on scans. A city wants to forecast bus demand. Each starts with a question and some data. Data science is the craft of connecting the two honestly."),
  T("Machine learning is a way to build programs from examples. Instead of writing the rule 'if the email says free money, it is spam', you show a model thousands of labelled emails and it finds the pattern itself. The examples are rows. The input columns are called features, and the answer column is the label or target."),
  T("There are three big families. In supervised learning, every training example comes with the right answer. If the answer is a number, such as a house price, the task is regression. If it is a category, such as spam or not spam, it is classification. In unsupervised learning there are no answers, and the goal is to find structure, for example groups of similar customers. A third family, reinforcement learning, learns by trial and reward."),
  T("The Python ecosystem is built in layers. NumPy provides fast multi-dimensional arrays. pandas builds tables, called DataFrames, on top. Matplotlib draws charts. scikit-learn offers dozens of machine learning methods with one consistent interface. Keras, part of TensorFlow, builds neural networks. You will meet them in this order."),
  C("import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nfrom sklearn.linear_model import LinearRegression\nfrom tensorflow import keras\n\ndf = pd.read_csv('houses.csv')\nprint(df.head())", "python"),
  T("A note about this course. The labs here run on the app's built-in Python, which does not include these libraries. So the lessons show you real library code to read and copy into your own notebook, while each lab rebuilds the core idea in plain Python: a dot product, a small table, a nearest-neighbour classifier, a neural neuron. Knowing how the machinery works makes you far better at using the libraries.")],
 [("What is a feature?", ["An input variable used for prediction", "The answer to predict", "A chart type", "A file"], 0, "A column of X."),
  ("What is a label?", ["The value we want to predict", "An input", "A plot", "A library"], 0, "The target y."),
  ("Which task predicts a number?", ["Regression", "Classification", "Clustering", "Sorting"], 0, "House price."),
  ("What is unsupervised learning?", ["Finding structure without labels", "Learning with answers", "Learning by reward", "Copying"], 0, "Clusters."),
  ("Which library gives DataFrames?", ["pandas", "Matplotlib", "Keras", "NumPy"], 0, "Tables."),
  ("Where does most project time go?", ["Preparing data", "Choosing the model", "Drawing logos", "Waiting"], 0, "Cleaning.")],
 [("X, y", "features and target"), ("df.head()", "first rows of a table"), ("import numpy as np", "standard import")],
 [ORDER("The data science workflow", "Put the steps of a typical project in order.", ["Ask a question", "Collect data", "Clean the data", "Explore and plot", "Build a model", "Evaluate honestly", "Communicate results"]),
  MATCH("Match the tool", "Pair each library with its role.", [("NumPy", "fast arrays"), ("pandas", "tables of data"), ("Matplotlib", "charts"), ("scikit-learn", "classic machine learning"), ("Keras", "neural networks")]),
  PL("Summary statistics", "Write summary(x): the list [mean, median, minimum, maximum] of a non-empty list of numbers, each rounded to 3 decimals.", "summary(x)", '''
def summary(x):
    s = sorted(x)
    n = len(s)
    if n % 2 == 1:
        med = s[n // 2]
    else:
        med = (s[n // 2 - 1] + s[n // 2]) / 2.0
    return [round(sum(x) / float(n), 3), round(med, 3), round(s[0], 3), round(s[-1], 3)]
''', [[[1, 2, 3, 4, 5]], [[10, 20]], [[3, 1, 2]], [[7]], [[1.5, 2.5, 10]]], "Sort for the median."),
  PL("Count categories", "Write counts(values): how many times each value appears, as a list of [value, count] pairs sorted by value.", "counts(values)", '''
def counts(values):
    d = {}
    for v in values:
        d[v] = d.get(v, 0) + 1
    out = []
    for k in sorted(d.keys()):
        out.append([k, d[k]])
    return out
''', [[['a', 'b', 'a', 'c', 'a']], [[3, 1, 3, 1, 2]], [[]]], "Use a dictionary then sort the keys."),
  PL("Task type", "Write task_type(target_values): return 'classification' if every target value is a string or a bool, otherwise 'regression'.", "task_type(target_values)", '''
def task_type(target_values):
    for v in target_values:
        if not (isinstance(v, str) or isinstance(v, bool)):
            return 'regression'
    return 'classification'
''', [[['spam', 'ham']], [[1.5, 2.5]], [[True, False]], [[10, 20, 30]]], "Strings and booleans are categories."),
  PL("Features and target", "Write split_xy(rows, target): rows is a list of dicts; return [X, y] where X is the list of lists of the other columns' values in sorted column-name order and y the list of target values.", "split_xy(rows, target)", '''
def split_xy(rows, target):
    X = []
    y = []
    for r in rows:
        cols = sorted([k for k in r.keys() if k != target])
        X.append([r[k] for k in cols])
        y.append(r[target])
    return [X, y]
''', [[[{'a': 1, 'b': 2, 'p': 10}, {'a': 3, 'b': 4, 'p': 20}], 'p'], [[{'x': 5, 'label': 'u'}], 'label']], "Split each row.")]
))

CHS.append(CH(
 "NumPy: arrays and vectorised thinking",
 ("NumPy", [
  "ndarray | holds | Numbers of one type",
  "Shape | gives | Dimensions",
  "Vectorisation | replaces | Loops",
  "Broadcasting | stretches | Small arrays",
  "Dot product | multiplies | And sums",
  "Axis | selects | Rows or columns",
  "Boolean mask | filters | Elements"]),
 ["A NumPy array stores numbers of one type in a compact block, so operations on whole arrays run in fast compiled code. Its shape tells how many rows, columns and so on.",
  "Vectorisation means writing a * 2 or a + b instead of a loop. Broadcasting lets arrays of different shapes combine, for example adding a row of column means to every row.",
  "Reductions such as sum, mean and std collapse an axis. Boolean masks select elements that meet a condition."],
 [("Array", "A grid of numbers of one type, indexed by position."),
  ("Shape", "The tuple of dimension sizes, such as (3, 4) for 3 rows and 4 columns."),
  ("Vectorisation", "Applying an operation to a whole array at once instead of with a Python loop."),
  ("Broadcasting", "The rule that lets arrays of different shapes be combined by stretching the smaller one."),
  ("Axis", "A dimension of an array; axis 0 runs down the rows, axis 1 across the columns.")],
 ["np.array([1, 2, 3]).",
  "a.shape, a.reshape(2, 3).",
  "a + b, a * 2, a ** 2 act element by element.",
  "a.mean(axis=0) averages each column.",
  "a[a > 0] keeps positive entries."],
 [T("Python lists are flexible but slow for maths, because each number is a separate object. A NumPy array is a tight block of numbers of one type. Adding two arrays of a million numbers takes a few milliseconds. The same loop in plain Python takes a second or more."),
  C("import numpy as np\na = np.array([[1, 2, 3], [4, 5, 6]])\nprint(a.shape)        # (2, 3)\nprint(a * 10)         # every element times 10\nprint(a.sum(axis=0))  # column sums: [5 7 9]\nprint(a.mean())       # 3.5", "python"),
  T("The shape of that array is two rows by three columns. Arithmetic works element by element, which we call vectorised. You write what you want for the whole array and let NumPy do the looping."),
  T("Broadcasting extends this to arrays of different sizes. If you subtract the column means, a row of three numbers, from a matrix with two rows and three columns, NumPy stretches the row down to fit. This is how data is centred and scaled in a single line: subtract the mean and divide by the standard deviation."),
  C("X = np.array([[1., 200.], [2., 300.], [3., 400.]])\nX_scaled = (X - X.mean(axis=0)) / X.std(axis=0)", "python"),
  T("The dot product is the heart of machine learning. Multiply two vectors element by element and add: that is one neuron, one linear model prediction. The matrix product does many of these at once, and is how a whole layer of a neural network is computed."),
  T("Boolean masks pick elements by condition. The expression a greater than 3 gives an array of true and false, and using it as an index keeps only the true entries. The labs build these operations by hand so you see what the array library does for you.")],
 [("Why are NumPy arrays fast?", ["Compact data and compiled loops", "They use less memory only", "They avoid maths", "They are shorter"], 0, "No Python loop."),
  ("What is the shape of a 2-row, 3-column array?", ["(2, 3)", "(3, 2)", "(6,)", "(1, 6)"], 0, "Rows first."),
  ("What does a.mean(axis=0) give?", ["The mean of each column", "The mean of each row", "One overall mean", "The shape"], 0, "Down the rows."),
  ("What is broadcasting?", ["Stretching small arrays to fit", "Printing arrays", "Sorting", "Copying files"], 0, "Shape rules."),
  ("What does a[a > 0] return?", ["The positive elements", "True and false values", "The count", "The mean"], 0, "A mask."),
  ("What does the dot product compute?", ["Multiply elementwise and sum", "Add all elements", "The largest element", "The shape"], 0, "One neuron.")],
 [("a @ b", "matrix product"), ("a.mean(axis=0)", "column means"), ("(X - mu) / sigma", "standardise")],
 [MATCH("Match the term", "Pair each NumPy idea with its meaning.", [("Shape", "dimension sizes"), ("Vectorisation", "whole-array operations"), ("Broadcasting", "stretching to fit"), ("Axis", "a direction in the array"), ("Mask", "true and false filter")]),
  PL("Dot product", "Write dot(a, b): the dot product of two equal-length lists.", "dot(a, b)", '''
def dot(a, b):
    s = 0
    for i in range(len(a)):
        s = s + a[i] * b[i]
    return s
''', [[[1, 2, 3], [4, 5, 6]], [[0, 0], [5, 7]], [[2], [3]], [[1, -1], [1, 1]]], "Multiply and add."),
  PL("Matrix product", "Write matmul(A, B): the product of matrix A (rows of lists) and matrix B.", "matmul(A, B)", '''
def matmul(A, B):
    out = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            s = 0
            for k in range(len(B)):
                s = s + A[i][k] * B[k][j]
            row.append(s)
        out.append(row)
    return out
''', [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], [[[1, 0], [0, 1]], [[9, 8], [7, 6]]], [[[1, 2, 3]], [[1], [2], [3]]]], "Row of A times column of B."),
  PL("Column means", "Write col_means(X): the mean of each column of the matrix X, rounded to 3 decimals.", "col_means(X)", '''
def col_means(X):
    out = []
    for j in range(len(X[0])):
        s = 0.0
        for i in range(len(X)):
            s = s + X[i][j]
        out.append(round(s / len(X), 3))
    return out
''', [[[[1, 2], [3, 4]]], [[[1, 200], [2, 300], [3, 400]]], [[[5]]]], "Sum down each column."),
  PL("Standardise columns", "Write standardise(X): subtract each column's mean and divide by its population standard deviation (if the standard deviation is 0 leave the column centred). Round to 3 decimals.", "standardise(X)", '''
import math
def standardise(X):
    n = len(X)
    m = len(X[0])
    out = []
    for i in range(n):
        out.append([0] * m)
    for j in range(m):
        mu = sum([X[i][j] for i in range(n)]) / float(n)
        var = sum([(X[i][j] - mu) ** 2 for i in range(n)]) / float(n)
        sd = math.sqrt(var)
        for i in range(n):
            v = X[i][j] - mu
            if sd > 0:
                v = v / sd
            out[i][j] = round(v, 3)
    return out
''', [[[[1, 200], [2, 300], [3, 400]]], [[[1, 5], [1, 7]]], [[[10, 0], [20, 0]]]], "Centre, then scale.", approx=None),
  PL("Add a row (broadcast)", "Write broadcast_add(X, row): add the list row to every row of the matrix X.", "broadcast_add(X, row)", '''
def broadcast_add(X, row):
    out = []
    for r in X:
        out.append([r[j] + row[j] for j in range(len(row))])
    return out
''', [[[[1, 2], [3, 4]], [10, 20]], [[[0, 0, 0]], [1, 2, 3]], [[[5], [6]], [1]]], "Match columns."),
  PL("Boolean mask", "Write keep_above(a, t): the elements of a that are greater than t, in order.", "keep_above(a, t)", '''
def keep_above(a, t):
    return [v for v in a if v > t]
''', [[[1, 5, 2, 8], 2], [[1, 2], 5], [[-1, 0, 1], -1]], "Filter by condition."),
  PL("Reshape", "Write reshape(flat, rows, cols): turn a flat list of rows x cols numbers into a list of rows lists, filling row by row.", "reshape(flat, rows, cols)", '''
def reshape(flat, rows, cols):
    out = []
    for i in range(rows):
        out.append(flat[i * cols:(i + 1) * cols])
    return out
''', [[[1, 2, 3, 4, 5, 6], 2, 3], [[1, 2, 3, 4, 5, 6], 3, 2], [[1, 2], 1, 2]], "Slice a row at a time.")]
))

CHS.append(CH(
 "pandas: tables of data",
 ("pandas", [
  "DataFrame | is | A table",
  "Series | is | A column",
  "Index | labels | Rows",
  "Filtering | selects | Rows by condition",
  "Groupby | summarises | Per category",
  "Missing values | are | NaN",
  "Merge | joins | Tables on a key"]),
 ["A pandas DataFrame is a table with named columns, and a Series is a single column. You load data with read_csv, look with head and info, and select with square brackets.",
  "Filtering uses conditions such as df[df.age > 30]. Groupby splits the table by a category, applies a summary such as mean to each group, and combines the answer.",
  "Real data has missing values, shown as NaN. You can drop rows, or fill the gaps with a mean, a median or a constant. Merge joins two tables on a shared key column."],
 [("DataFrame", "A two-dimensional labelled table of data with columns of possibly different types."),
  ("Series", "A one-dimensional labelled array, such as one column of a DataFrame."),
  ("groupby", "Splitting rows into groups by a key, applying a function to each, and combining the results."),
  ("NaN", "Not a number; the marker for a missing value."),
  ("merge", "Combining two tables by matching values in a key column.")],
 ["df['col'] is a Series; df[['a', 'b']] a DataFrame.",
  "df[df.price > 100] filters rows.",
  "df.groupby('city')['price'].mean().",
  "df.isna().sum() counts missing values.",
  "pd.merge(a, b, on='id')."],
 [T("A spreadsheet has rows and columns; a pandas DataFrame is the programmer's version. Each column has a name and a type, each row an index. It is the workhorse of data science because real data nearly always arrives as a table."),
  C("import pandas as pd\ndf = pd.DataFrame({\n    'city': ['Paris', 'Rome', 'Paris', 'Rome'],\n    'price': [300, 250, 340, None],\n})\nprint(df.describe())\nprint(df[df['price'] > 260])\nprint(df.groupby('city')['price'].mean())", "python"),
  T("Selecting a single column gives a Series. Selecting with a condition gives the rows where it is true. The command groupby city and then mean price splits the table into a Paris group and a Rome group and averages each. This split, apply, combine pattern answers most business questions."),
  T("Look at that table again: one price is missing. Missing values appear everywhere, from broken sensors to skipped survey questions. pandas shows them as NaN and most summaries skip them, but models usually cannot cope. You must decide: drop the rows, fill with the column mean or median, or fill with a typical value for that group. Each choice has consequences, so note it."),
  C("df['price'] = df['price'].fillna(df['price'].median())\nrent = pd.DataFrame({'city': ['Paris', 'Rome'], 'country': ['FR', 'IT']})\nfull = pd.merge(df, rent, on='city')", "python"),
  T("Merge joins two tables that share a key, like a customers table and an orders table. An inner join keeps only matching keys. The labs here use a list of dictionaries as a tiny DataFrame, one dictionary per row, so you can build selection, groupby, filling and merge yourself.")],
 [("What is a Series?", ["One column of a table", "A whole table", "A chart", "A model"], 0, "1D labelled."),
  ("What does groupby do?", ["Split, apply, combine", "Sort a list", "Draw a plot", "Delete rows"], 0, "Per-category summary."),
  ("How is a missing value shown?", ["NaN", "-1", "Zero", "Blank text only"], 0, "Not a number."),
  ("How do you keep rows with price above 100?", ["df[df.price > 100]", "df.price > 100 = True", "df.keep(100)", "df.drop(100)"], 0, "Boolean mask."),
  ("What does merge do?", ["Joins tables on a key", "Sorts a table", "Fits a model", "Scales columns"], 0, "Like SQL join."),
  ("Name one way to handle missing data.", ["Fill with the median", "Delete the column header", "Add more NaN", "Ignore it silently"], 0, "Impute.")],
 [("df.head()", "first rows"), ("df.describe()", "summary statistics"), ("df.groupby(k)[c].mean()", "group means")],
 [MATCH("Match the term", "Pair each pandas idea with its meaning.", [("DataFrame", "table"), ("Series", "column"), ("groupby", "split, apply, combine"), ("NaN", "missing value"), ("merge", "join on a key")]),
  PL("Select columns", "Write select(rows, cols): rows is a list of dicts; return a list of dicts containing only the listed columns.", "select(rows, cols)", '''
def select(rows, cols):
    out = []
    for r in rows:
        out.append({c: r[c] for c in cols})
    return out
''', [[[{'a': 1, 'b': 2, 'c': 3}, {'a': 4, 'b': 5, 'c': 6}], ['a', 'c']], [[{'x': 1}], ['x']]], "Build a smaller dict."),
  PL("Filter rows", "Write filter_rows(rows, col, minimum): rows is a list of dicts; return the list of row indexes whose value in col is at least minimum.", "filter_rows(rows, col, minimum)", '''
def filter_rows(rows, col, minimum):
    return [i for i in range(len(rows)) if rows[i][col] >= minimum]
''', [[[{'n': 'a', 'v': 3}, {'n': 'b', 'v': 10}], 'v', 5], [[{'v': 1}], 'v', 1], [[{'v': 1}], 'v', 2]], "Collect the indexes that pass."),
  PL("Group mean", "Write group_mean(rows, key, col): the mean of col for each distinct key, as a list of [key, mean] pairs sorted by key, means rounded to 2 decimals.", "group_mean(rows, key, col)", '''
def group_mean(rows, key, col):
    sums = {}
    cnt = {}
    for r in rows:
        k = r[key]
        sums[k] = sums.get(k, 0) + r[col]
        cnt[k] = cnt.get(k, 0) + 1
    out = []
    for k in sorted(sums.keys()):
        out.append([k, round(sums[k] / float(cnt[k]), 2)])
    return out
''', [[[{'c': 'P', 'p': 300}, {'c': 'R', 'p': 250}, {'c': 'P', 'p': 340}], 'c', 'p'], [[{'c': 'A', 'p': 1}], 'c', 'p']], "Sum and count per key."),
  PL("Fill missing", "Write fill_mean(rows, col): replace None values of col with the mean of the non-missing values (rounded to 2 decimals). Return the new list of dicts.", "fill_mean(rows, col)", '''
def fill_mean(rows, col):
    vals = [r[col] for r in rows if r[col] is not None]
    m = round(sum(vals) / float(len(vals)), 2)
    out = []
    for r in rows:
        d = dict(r)
        if d[col] is None:
            d[col] = m
        out.append(d)
    return out
''', [[[{'p': 300}, {'p': None}, {'p': 340}], 'p'], [[{'p': 1}, {'p': 2}, {'p': None}, {'p': None}], 'p']], "Average the known values first."),
  PL("Inner merge", "Write merge(left, right): inner join of two small tables where every row is a [key, value] pair. For each left row, for each right row with the same key, output [key, left_value, right_value], in left then right order.", "merge(left, right)", '''
def merge(left, right):
    out = []
    for a in left:
        for b in right:
            if a[0] == b[0]:
                out.append([a[0], a[1], b[1]])
    return out
''', [[[['P', 1], ['R', 2], ['X', 3]], [['P', 'FR'], ['R', 'IT']]], [[['A', 1]], [['B', 2]]], [[['P', 1], ['P', 2]], [['P', 'x']]]], "Nested loops matching the key."),
  PL("Sort by column", "Write sort_by(rows, col, descending): the values of col sorted; if descending is True largest first.", "sort_by(rows, col, descending)", '''
def sort_by(rows, col, descending):
    return sorted([r[col] for r in rows], reverse=descending)
''', [[[{'v': 2}, {'v': 1}, {'v': 3}], 'v', False], [[{'v': 2}, {'v': 1}, {'v': 3}], 'v', True]], "Use sorted with a key function.")]
))

CHS.append(CH(
 "Matplotlib and exploring data",
 ("Exploration", [
  "Histogram | shows | Distribution",
  "Scatter plot | shows | Relationship",
  "Line plot | shows | Trend",
  "Correlation | measures | Linear link",
  "Outlier | is | Unusual value",
  "Quartile | splits | Sorted data",
  "EDA | comes | Before modelling"]),
 ["Exploratory data analysis (EDA) means looking at the data before modelling. Matplotlib draws the basic charts: line plots for trends, scatter plots for relationships between two variables, histograms for distributions and bar charts for categories.",
  "Summary numbers complement plots: the mean and median, the standard deviation, quartiles and the correlation coefficient between two variables.",
  "Outliers, skewed distributions and surprises found now save trouble later. Always plot before you model."],
 [("EDA", "Exploratory data analysis: summarising and visualising data to understand it."),
  ("Histogram", "A chart that counts how many values fall in each bin."),
  ("Correlation", "A number from -1 to 1 measuring how closely two variables move together in a straight line."),
  ("Quartile", "A value that splits sorted data into quarters; Q1 is the 25th percentile, Q3 the 75th."),
  ("Outlier", "A value far from the rest, often defined as beyond 1.5 times the interquartile range from the quartiles.")],
 ["plt.plot(x, y); plt.scatter(x, y); plt.hist(x, bins=10).",
  "Always label axes and add a title.",
  "r = covariance / (sd_x sd_y).",
  "IQR = Q3 - Q1.",
  "Correlation is not causation."],
 [T("Before building any model, look at the data. A table of numbers hides patterns that a chart shows at once. Matplotlib is Python's drawing library. The pyplot interface works like a sketchpad: make a figure, plot, label, show."),
  C("import matplotlib.pyplot as plt\nplt.figure(figsize=(6, 4))\nplt.scatter(df['area'], df['price'], alpha=0.6)\nplt.xlabel('Area (m2)')\nplt.ylabel('Price (k)')\nplt.title('Price against area')\nplt.show()\n\nplt.hist(df['price'], bins=20)", "python"),
  T("Choose the chart for the question. Is there a trend over time? Line plot. Do two numbers move together? Scatter plot. How are the values of one variable spread? Histogram or box plot. How do categories compare? Bar chart. Good charts have labelled axes, units and a title that says what to notice."),
  T("The correlation coefficient puts a number on the straight-line link between two variables. It runs from minus one, perfect opposite movement, through zero, no linear link, to plus one, perfect together movement. It misses curved relationships, and it says nothing about cause: ice cream sales and drownings both rise in summer."),
  T("Outliers can be mistakes, such as an age of 999, or real rare events. A common rule flags values more than one and a half interquartile ranges beyond the quartiles. Decide case by case whether to fix, remove or keep them, and write down why. In the plot explorer you can look at several datasets and see correlation and outliers directly.")],
 [("Which chart shows a distribution?", ["Histogram", "Line plot", "Pie chart of two numbers", "Table"], 0, "Counts per bin."),
  ("Which chart shows a relationship between two numbers?", ["Scatter plot", "Histogram", "Bar chart", "Pie chart"], 0, "Points."),
  ("What does a correlation of -1 mean?", ["Perfect opposite linear movement", "No link", "Perfect same movement", "An error"], 0, "Straight downhill."),
  ("What does correlation not show?", ["Causation", "Direction", "Strength", "Sign"], 0, "Confounders."),
  ("What is the IQR?", ["Q3 minus Q1", "Max minus min", "Mean minus median", "Q1 plus Q3"], 0, "Middle half."),
  ("What is EDA?", ["Looking at data before modelling", "Deleting data", "A model type", "A chart type"], 0, "Exploration.")],
 [("plt.scatter(x, y)", "scatter plot"), ("IQR = Q3 - Q1", "spread of the middle half"), ("r in [-1, 1]", "correlation range")],
 [APP("PLOT", "Plot explorer", "Choose a dataset and a chart, and read the summary numbers. Look at at least three different datasets and the correlation and outlier readout for each to complete the lab.", 780),
  MATCH("Match the chart", "Pair each chart with its question.", [("Line plot", "trend over time"), ("Scatter plot", "relationship of two numbers"), ("Histogram", "distribution of one number"), ("Bar chart", "compare categories"), ("Box plot", "median and spread")]),
  PL("Histogram counts", "Write hist(x, lo, hi, nbins): split the range lo..hi into nbins equal bins and count how many values fall in each (a value equal to hi goes in the last bin; values outside the range are ignored). Return the list of counts.", "hist(x, lo, hi, nbins)", '''
def hist(x, lo, hi, nbins):
    counts = [0] * nbins
    w = (hi - lo) / float(nbins)
    for v in x:
        if v < lo or v > hi:
            continue
        i = int((v - lo) / w)
        if i >= nbins:
            i = nbins - 1
        counts[i] = counts[i] + 1
    return counts
''', [[[1, 2, 2, 3, 9, 10], 0, 10, 5], [[0, 5, 10], 0, 10, 2], [[1, 1, 1], 0, 4, 4], [[-5, 15], 0, 10, 2]], "Compute the bin index with the bin width."),
  PL("Correlation", "Write corr(x, y): the Pearson correlation coefficient of two equal-length lists, rounded to 3 decimals.", "corr(x, y)", '''
import math
def corr(x, y):
    n = len(x)
    mx = sum(x) / float(n)
    my = sum(y) / float(n)
    sxy = 0.0
    sxx = 0.0
    syy = 0.0
    for i in range(n):
        sxy = sxy + (x[i] - mx) * (y[i] - my)
        sxx = sxx + (x[i] - mx) ** 2
        syy = syy + (y[i] - my) ** 2
    return round(sxy / math.sqrt(sxx * syy), 3)
''', [[[1, 2, 3, 4], [2, 4, 6, 8]], [[1, 2, 3, 4], [8, 6, 4, 2]], [[1, 2, 3, 4, 5], [2, 1, 4, 3, 5]], [[1, 2, 3], [5, 5.5, 5.2]]], "Covariance over the product of spreads.", approx=0.002),
  PL("Quantile", "Write quantile(x, q): the q-quantile (0 to 1) of x with linear interpolation: sort, position = q x (n - 1), interpolate between the neighbouring values. Round to 3 decimals.", "quantile(x, q)", '''
def quantile(x, q):
    s = sorted(x)
    pos = q * (len(s) - 1)
    lo = int(pos)
    hi = lo + 1
    if hi >= len(s):
        return round(float(s[lo]), 3)
    frac = pos - lo
    return round(s[lo] + frac * (s[hi] - s[lo]), 3)
''', [[[1, 2, 3, 4, 5], 0.5], [[1, 2, 3, 4], 0.25], [[10, 20, 30, 40], 0.75], [[5], 0.9]], "Interpolate between sorted neighbours.", approx=0.002),
  PL("Outliers by IQR", "Write outliers(x): the values more than 1.5 x IQR below Q1 or above Q3 (quartiles by linear interpolation as in quantile), in original order.", "outliers(x)", '''
def outliers(x):
    s = sorted(x)
    def q(p):
        pos = p * (len(s) - 1)
        lo = int(pos)
        if lo + 1 >= len(s):
            return float(s[lo])
        return s[lo] + (pos - lo) * (s[lo + 1] - s[lo])
    q1 = q(0.25)
    q3 = q(0.75)
    iqr = q3 - q1
    lo = q1 - 1.5 * iqr
    hi = q3 + 1.5 * iqr
    return [v for v in x if v < lo or v > hi]
''', [[[1, 2, 3, 4, 5, 100]], [[10, 12, 11, 13, 12]], [[-50, 1, 2, 3, 4]]], "Compute the fences, then filter."),
  PL("Describe", "Write describe(x): the list [count, mean, population std, min, max] of a non-empty list, each rounded to 3 decimals.", "describe(x)", '''
import math
def describe(x):
    n = len(x)
    m = sum(x) / float(n)
    var = sum([(v - m) ** 2 for v in x]) / float(n)
    return [n, round(m, 3), round(math.sqrt(var), 3), round(min(x), 3), round(max(x), 3)]
''', [[[1, 2, 3, 4]], [[5]], [[2, 4, 4, 4, 5, 5, 7, 9]]], "Population standard deviation divides by n.", approx=0.002)]
))

CHS.append(CH(
 "Preparing data for models",
 ("Preparation", [
  "Cleaning | fixes | Errors and gaps",
  "Encoding | turns | Categories into numbers",
  "One-hot | makes | Indicator columns",
  "Scaling | equalises | Feature ranges",
  "Train-test split | holds out | Honest data",
  "Leakage | spoils | Evaluation",
  "Pipeline | chains | Steps"]),
 ["Models need numbers, in sensible ranges, with no gaps. Preparation fills or removes missing values, converts categories to numbers (one-hot encoding), and scales features so large-valued columns do not dominate.",
  "Before anything is fitted, split the data into a training set to learn from and a test set held back for an honest score.",
  "Data leakage is when information from outside the training data sneaks in, such as scaling with statistics from the test set. It gives scores that are too good to be true. Pipelines keep every step inside training."],
 [("One-hot encoding", "Turning a categorical column into several 0/1 columns, one per category."),
  ("Scaling", "Rescaling a feature, for example to mean 0 and standard deviation 1, or to the range 0 to 1."),
  ("Training set", "The data a model learns from."),
  ("Test set", "Held-out data used once at the end to estimate performance on new data."),
  ("Data leakage", "Using information in training that would not be available at prediction time.")],
 ["X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0).",
  "Fit the scaler on training data only.",
  "One-hot: one column per category.",
  "Impute with the training median.",
  "Pipeline = preprocessing + model."],
 [T("Raw data is rarely ready for a model. A column of cities cannot be multiplied by a weight. A salary in thousands dwarfs an age in tens. A missing value stops many algorithms. Preparation fixes these before learning starts, and it affects results as much as the model choice."),
  T("Categories become numbers by one-hot encoding. A column city with values Paris, Rome and Oslo becomes three columns, is_Paris, is_Rome and is_Oslo, each zero or one. This avoids implying that Rome is somehow twice Paris. Scaling puts features on similar ranges. Standardising subtracts the mean and divides by the standard deviation. Min-max scaling squeezes the values to between zero and one."),
  C("from sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler, OneHotEncoder\nfrom sklearn.impute import SimpleImputer\n\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42)\nscaler = StandardScaler().fit(X_train)   # learn mean and std from training only\nX_train_s = scaler.transform(X_train)\nX_test_s = scaler.transform(X_test)", "python"),
  T("Here comes the most important rule of the course. The test set stands for the future, data your model has never seen. If anything about the test set influences training, including its mean used for scaling, your score is no longer honest. That is data leakage. Fit scalers, imputers and encoders on the training data only, and then apply them to the test data."),
  T("A pipeline chains the steps and the model into one object, so that fitting happens in the right order and, with cross-validation, in every fold. It also makes your work repeatable. The labs implement encoders, scalers, a seeded shuffle and a split, so you can see that they are only a few lines each.")],
 [("What does one-hot encoding do?", ["Makes a 0/1 column per category", "Scales a column", "Fills gaps", "Sorts rows"], 0, "Indicators."),
  ("Why scale features?", ["So large ranges do not dominate", "To remove labels", "To add noise", "To sort"], 0, "Fair comparison."),
  ("What is the test set for?", ["An honest final estimate", "Training", "Tuning every time", "Plotting"], 0, "Unseen data."),
  ("What is data leakage?", ["Test information influencing training", "Losing a file", "A slow model", "Too many columns"], 0, "Too-good scores."),
  ("Where should a scaler be fitted?", ["On training data only", "On all data", "On test data", "Nowhere"], 0, "No peeking."),
  ("What is a pipeline for?", ["Chaining preprocessing and model safely", "Drawing plots", "Storing data", "Sorting"], 0, "Order and repeatability.")],
 [("(x - mean) / std", "standardise"), ("(x - min) / (max - min)", "min-max"), ("fit on train, transform both", "leak-free scaling")],
 [MATCH("Match the term", "Pair each step with its job.", [("Imputation", "fill missing values"), ("One-hot encoding", "categories to indicator columns"), ("Scaling", "similar feature ranges"), ("Train-test split", "hold back honest data"), ("Pipeline", "chained steps")]),
  PL("One-hot encode", "Write one_hot(values, categories): for each value return a list of 0/1 with a 1 at the position of the value in categories.", "one_hot(values, categories)", '''
def one_hot(values, categories):
    out = []
    for v in values:
        out.append([1 if v == c else 0 for c in categories])
    return out
''', [[['Paris', 'Rome', 'Paris'], ['Oslo', 'Paris', 'Rome']], [['a'], ['a', 'b']], [[], ['a']]], "One column per category."),
  PL("Min-max scale", "Write min_max(x): rescale a list to the range 0 to 1 using (v - min) / (max - min), rounded to 3 decimals. If all values are equal return zeros.", "min_max(x)", '''
def min_max(x):
    lo = min(x)
    hi = max(x)
    if hi == lo:
        return [0.0] * len(x)
    return [round((v - lo) / float(hi - lo), 3) for v in x]
''', [[[1, 2, 3, 5]], [[10, 10]], [[-1, 0, 1]], [[100, 200]]], "Shift then divide by the range."),
  PL("Leak-free scaling", "Write scale_split(train, test): standardise both lists using the mean and population standard deviation of train only. Return [scaled_train, scaled_test], each value rounded to 3 decimals.", "scale_split(train, test)", '''
import math
def scale_split(train, test):
    m = sum(train) / float(len(train))
    sd = math.sqrt(sum([(v - m) ** 2 for v in train]) / float(len(train)))
    a = [round((v - m) / sd, 3) for v in train]
    b = [round((v - m) / sd, 3) for v in test]
    return [a, b]
''', [[[1, 2, 3], [4, 5]], [[10, 20, 30, 40], [25]], [[0, 2], [1, 3]]], "Use the training mean and std for the test values too.", approx=None),
  PL("Seeded shuffle", "Write shuffled(n, seed): the list 0..n-1 shuffled by this procedure: state = seed; for i from n-1 down to 1: state = (state x 1103515245 + 12345) mod 2147483648; j = state mod (i + 1); swap items i and j.", "shuffled(n, seed)", '''
def shuffled(n, seed):
    a = list(range(n))
    state = seed
    for i in range(n - 1, 0, -1):
        state = (state * 1103515245 + 12345) % 2147483648
        j = state % (i + 1)
        t = a[i]
        a[i] = a[j]
        a[j] = t
    return a
''', [[5, 1], [8, 42], [3, 0], [1, 7]], "Fisher-Yates with a simple generator."),
  PL("Train-test split", "Write split(rows, test_fraction, seed): shuffle the indexes 0..n-1 with the seeded shuffle above, take the first int(n x test_fraction) shuffled indexes as the test set and the rest as training. Return [train_rows, test_rows] keeping each group's rows in the shuffled order.", "split(rows, test_fraction, seed)", '''
def split(rows, test_fraction, seed):
    n = len(rows)
    a = list(range(n))
    state = seed
    for i in range(n - 1, 0, -1):
        state = (state * 1103515245 + 12345) % 2147483648
        j = state % (i + 1)
        t = a[i]
        a[i] = a[j]
        a[j] = t
    k = int(n * test_fraction)
    test = [rows[i] for i in a[:k]]
    train = [rows[i] for i in a[k:]]
    return [train, test]
''', [[[10, 20, 30, 40, 50], 0.4, 3], [['a', 'b', 'c', 'd'], 0.25, 9], [[1, 2, 3], 0.0, 1]], "Reuse the shuffle, then slice."),
  PL("Median imputation", "Write impute_median(x): replace None entries by the median of the non-missing values (for an even count take the mean of the middle two). Return the new list.", "impute_median(x)", '''
def impute_median(x):
    v = sorted([a for a in x if a is not None])
    n = len(v)
    if n % 2 == 1:
        m = v[n // 2]
    else:
        m = (v[n // 2 - 1] + v[n // 2]) / 2.0
    return [m if a is None else a for a in x]
''', [[[1, None, 3, 10]], [[5, 5, None]], [[None, 2, 4]]], "Median of the known values.")]
))

CHS.append(CH(
 "Linear regression and the scikit-learn way",
 ("Regression", [
  "Regression | predicts | A number",
  "Linear model | uses | Weights",
  "Least squares | minimises | Squared error",
  "Gradient descent | follows | The slope",
  "R squared | measures | Fit quality",
  "fit | learns | From data",
  "predict | applies | The model"]),
 ["Linear regression predicts a number as a weighted sum of features plus an intercept. Least squares picks the weights that minimise the sum of squared errors between predictions and true values.",
  "Every scikit-learn model follows the same pattern: create the model, call fit on training data, call predict on new data, and call score to evaluate.",
  "The quality of a regression is measured by mean squared error (average squared mistake) and R squared (the fraction of variation explained, up to 1)."],
 [("Linear regression", "A model predicting y = w x + b, fitted by minimising squared error."),
  ("Mean squared error (MSE)", "The average of the squared differences between predictions and truth."),
  ("R squared", "One minus the ratio of the model's squared error to that of always predicting the mean; 1 is perfect, 0 is no better than the mean."),
  ("Gradient descent", "Repeatedly nudging the parameters opposite to the gradient of the loss to reduce it."),
  ("Estimator", "A scikit-learn object with fit and predict methods.")],
 ["model = LinearRegression(); model.fit(X_train, y_train).",
  "y_pred = model.predict(X_test).",
  "slope = cov(x, y) / var(x); intercept = mean_y - slope mean_x.",
  "MSE = mean((y - y_pred)^2).",
  "R2 = 1 - SSE / SST."],
 [T("Suppose house price rises with floor area. The simplest model draws the best straight line through the points: price equals slope times area plus intercept. But 'best' needs a definition. Least squares says: choose the line whose total squared vertical distances to the points are smallest."),
  T("For one feature the answer has a neat formula. The slope is the covariance of x and y divided by the variance of x, and the intercept makes the line pass through the mean point. With many features it is still a linear algebra problem, solved by the normal equations or by gradient descent, which is also how neural networks learn."),
  C("from sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import mean_squared_error, r2_score\n\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\nprint(model.coef_, model.intercept_)\ny_pred = model.predict(X_test)\nprint(mean_squared_error(y_test, y_pred), r2_score(y_test, y_pred))", "python"),
  T("This shows the scikit-learn way. Every estimator has the same methods: fit to learn from X and y, predict to use what was learned. Swap LinearRegression for another model and the rest of your code stays the same. That uniform interface is why scikit-learn is so pleasant."),
  T("Gradient descent deserves a picture: stand on a hillside in fog and take small steps downhill. The loss as a function of the slope and intercept is a bowl, and each step moves along the steepest descent, scaled by the learning rate. Too small a rate is slow, too large overshoots. The regression lab lets you click points and watch the line settle, and the labs have you compute every step by hand.")],
 [("What does least squares minimise?", ["The sum of squared errors", "The sum of errors", "The number of features", "The slope"], 0, "Squared."),
  ("What is R squared of 1?", ["A perfect fit", "No fit", "A negative fit", "An error"], 0, "All variation explained."),
  ("What does fit do?", ["Learns from data", "Draws a plot", "Predicts on new data", "Loads a file"], 0, "Training."),
  ("What is the learning rate?", ["The step size of gradient descent", "The accuracy", "The number of rows", "The intercept"], 0, "Too big overshoots."),
  ("What is the slope formula for one feature?", ["cov(x, y) / var(x)", "mean(x) / mean(y)", "var(y)", "max(y) - min(y)"], 0, "Covariance over variance."),
  ("What is MSE?", ["Average squared error", "Average error", "Largest error", "Sum of features"], 0, "Penalises big mistakes.")],
 [("y = w x + b", "linear model"), ("w = w - lr x dL/dw", "gradient step"), ("R2 = 1 - SSE/SST", "R squared")],
 [APP("REG", "Regression playground", "Click to add points, then press Fit to see the least-squares line, MSE and R squared. Add at least six points and fit the line to complete this lab; try an outlier to see its pull.", 780),
  MATCH("Match the term", "Pair each term with its meaning.", [("fit", "learn from training data"), ("predict", "apply to new data"), ("MSE", "average squared error"), ("R squared", "fraction of variation explained"), ("Gradient descent", "step downhill on the loss")]),
  PL("Fit a line", "Write fit_line(x, y): the least-squares [slope, intercept] for one feature, rounded to 4 decimals.", "fit_line(x, y)", '''
def fit_line(x, y):
    n = len(x)
    mx = sum(x) / float(n)
    my = sum(y) / float(n)
    num = 0.0
    den = 0.0
    for i in range(n):
        num = num + (x[i] - mx) * (y[i] - my)
        den = den + (x[i] - mx) ** 2
    slope = num / den
    return [round(slope, 4), round(my - slope * mx, 4)]
''', [[[1, 2, 3, 4], [2, 4, 6, 8]], [[1, 2, 3], [3, 5, 4]], [[0, 10], [5, 25]], [[1, 2, 3, 4, 5], [10, 8, 6, 4, 2]]], "Covariance over variance.", approx=0.0002),
  PL("Predict", "Write predict(x, slope, intercept): the predictions slope x v + intercept for each v in x, rounded to 3 decimals.", "predict(x, slope, intercept)", '''
def predict(x, slope, intercept):
    return [round(slope * v + intercept, 3) for v in x]
''', [[[1, 2, 3], 2, 1], [[0], 0.5, 4], [[-1, 1], 3, 0]], "Apply the line."),
  PL("Mean squared error", "Write mse(y, y_pred): the mean of the squared differences, rounded to 4 decimals.", "mse(y, y_pred)", '''
def mse(y, y_pred):
    s = 0.0
    for i in range(len(y)):
        s = s + (y[i] - y_pred[i]) ** 2
    return round(s / len(y), 4)
''', [[[1, 2, 3], [1, 2, 4]], [[0, 0], [1, -1]], [[5], [5]]], "Square, add, divide.", approx=0.0002),
  PL("R squared", "Write r2(y, y_pred): 1 - SSE / SST, where SSE is the sum of squared errors of the predictions and SST the sum of squared differences of y from its mean. Round to 4 decimals.", "r2(y, y_pred)", '''
def r2(y, y_pred):
    m = sum(y) / float(len(y))
    sse = sum([(y[i] - y_pred[i]) ** 2 for i in range(len(y))])
    sst = sum([(v - m) ** 2 for v in y])
    return round(1 - sse / sst, 4)
''', [[[1, 2, 3, 4], [1, 2, 3, 4]], [[1, 2, 3, 4], [2.5, 2.5, 2.5, 2.5]], [[3, 5, 4], [3.5, 4.5, 4]]], "Compare with predicting the mean.", approx=0.0002),
  PL("Gradient descent", "Fit y = w x with gradient descent on the mean squared error: start w = 0; for each of steps iterations, gradient = mean of -2 x (y - w x) over the data, then w = w - lr x gradient. Write grad_descent(x, y, lr, steps) returning w rounded to 3 decimals.", "grad_descent(x, y, lr, steps)", '''
def grad_descent(x, y, lr, steps):
    w = 0.0
    n = len(x)
    for s in range(steps):
        g = 0.0
        for i in range(n):
            g = g + (-2.0 * x[i] * (y[i] - w * x[i]))
        g = g / n
        w = w - lr * g
    return round(w, 3)
''', [[[1, 2, 3], [2, 4, 6], 0.05, 100], [[1, 2], [3, 6], 0.1, 50], [[1, 2, 3], [1, 2, 3], 0.01, 10]], "Compute the average gradient, then step.", approx=0.01),
  PL("Multi-feature prediction", "Write predict_multi(X, weights, bias): for each row of features, the dot product with weights plus bias, rounded to 3 decimals.", "predict_multi(X, weights, bias)", '''
def predict_multi(X, weights, bias):
    out = []
    for row in X:
        s = bias
        for j in range(len(weights)):
            s = s + weights[j] * row[j]
        out.append(round(s, 3))
    return out
''', [[[[1, 2], [3, 4]], [0.5, 1.5], 2], [[[10]], [0.1], 0], [[[0, 0, 0]], [1, 2, 3], 7]], "Weighted sum plus intercept.")]
))
