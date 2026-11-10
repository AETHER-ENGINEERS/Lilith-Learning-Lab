# -*- coding: utf-8 -*-
"""Data science and ML course, part 2: classification, validation, clustering, neural networks, practice."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Classification: logistic regression, k-NN and trees",
 ("Classification", [
  "Classifier | predicts | A category",
  "Logistic regression | outputs | A probability",
  "Sigmoid | squashes | To 0..1",
  "k-NN | votes | Among neighbours",
  "Decision tree | asks | Yes/no questions",
  "Confusion matrix | counts | Hits and misses",
  "Precision recall | trade off | Errors"]),
 ["A classifier predicts a category. Logistic regression computes a weighted sum, passes it through the sigmoid function to get a probability between 0 and 1, and predicts the class if that exceeds a threshold.",
  "k-nearest neighbours predicts by letting the k closest training points vote. Decision trees ask a sequence of yes/no questions about features, choosing questions that best separate the classes.",
  "Accuracy is not enough. The confusion matrix and the measures precision, recall and F1 show what kinds of mistakes a model makes, which matters when classes are imbalanced."],
 [("Sigmoid", "The function 1 / (1 + e^(-z)) that squashes any number into the range 0 to 1."),
  ("k-nearest neighbours", "A method that classifies a point by majority vote among the k closest training points."),
  ("Decision tree", "A model of nested yes/no questions on features that ends in a prediction."),
  ("Precision", "Of the items predicted positive, the fraction that truly are positive."),
  ("Recall", "Of the truly positive items, the fraction the model found.")],
 ["LogisticRegression().fit(X, y).",
  "p = 1 / (1 + exp(-(w.x + b))).",
  "precision = TP / (TP + FP).",
  "recall = TP / (TP + FN).",
  "F1 = 2 P R / (P + R)."],
 [T("Is this email spam? Will this customer leave? Is this tumour malignant? These are classification questions, and the answer is a category. The simplest case has two classes, called positive and negative."),
  T("Logistic regression is a linear model with a twist. It forms the weighted sum of the features, then squeezes it through the sigmoid, an S-shaped curve that turns any number into a probability. Large positive sums give probabilities near one, large negative sums near zero. The decision boundary is where the probability is one half, a straight line in feature space."),
  C("from sklearn.linear_model import LogisticRegression\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import classification_report\n\nfor model in [LogisticRegression(), KNeighborsClassifier(n_neighbors=5), DecisionTreeClassifier(max_depth=3)]:\n    model.fit(X_train, y_train)\n    print(model.__class__.__name__, model.score(X_test, y_test))\nprint(classification_report(y_test, model.predict(X_test)))", "python"),
  T("k-nearest neighbours needs no training at all. To classify a new point, find the k closest points in the training data and take a vote. A small k follows the data closely and can chase noise. A large k smooths and can blur real boundaries. A decision tree instead learns questions such as 'is income above 40?', choosing at each step the question that makes the groups purest, measured by Gini impurity or entropy."),
  T("Do not trust accuracy alone. Imagine a disease that affects one patient in a hundred. A model that always says healthy is ninety-nine percent accurate and completely useless. The confusion matrix counts true positives, false positives, false negatives and true negatives. Precision asks how many alarms were right. Recall asks how many real cases were caught. F1 combines the two."),
  T("Which matters more depends on the cost. In cancer screening a missed case is far worse than a false alarm, so we want high recall. For a spam filter, losing a real email is worse than seeing some spam, so we want high precision. Move the decision threshold and you trade one for the other. The k-NN lab lets you see boundaries change with k.")],
 [("What does the sigmoid output?", ["A number between 0 and 1", "Any number", "A category name", "A distance"], 0, "A probability."),
  ("How does k-NN classify?", ["By vote of the nearest points", "By a formula", "By random choice", "By sorting"], 0, "Neighbours."),
  ("What does a small k risk?", ["Chasing noise", "Over-smoothing", "Nothing", "Slow training"], 0, "Overfitting."),
  ("What is recall?", ["Fraction of true positives found", "Fraction of alarms that were right", "Overall accuracy", "The threshold"], 0, "TP / (TP + FN)."),
  ("Why is accuracy misleading?", ["With imbalanced classes", "It is always wrong", "It is slow", "It needs labels"], 0, "Always say healthy."),
  ("What does a decision tree choose at each split?", ["The purest separation", "A random question", "The first column", "The longest word"], 0, "Gini or entropy.")],
 [("1 / (1 + e^-z)", "sigmoid"), ("TP, FP, FN, TN", "confusion matrix counts"), ("Gini = 1 - sum p^2", "impurity")],
 [APP("KNN", "k-NN boundary explorer", "Pick a dataset and a value of k, and see how the decision regions change. Try a very small k, a very large k and a middle value to complete the lab.", 780),
  MATCH("Match the metric", "Pair each metric with its meaning.", [("Accuracy", "fraction of all predictions right"), ("Precision", "alarms that were right"), ("Recall", "real cases that were caught"), ("F1", "balance of precision and recall"), ("Confusion matrix", "table of hits and misses")]),
  PL("Sigmoid", "Write sigmoid(z): 1 / (1 + e^(-z)), rounded to 4 decimals.", "sigmoid(z)", '''
import math
def sigmoid(z):
    return round(1.0 / (1.0 + math.exp(-z)), 4)
''', [[0], [2], [-2], [10], [-10]], "Use math.exp.", approx=0.0002),
  PL("Logistic prediction", "Write predict_proba(x, w, b): the probability sigmoid(w.x + b) of the positive class, rounded to 4 decimals.", "predict_proba(x, w, b)", '''
import math
def predict_proba(x, w, b):
    z = b
    for i in range(len(w)):
        z = z + w[i] * x[i]
    return round(1.0 / (1.0 + math.exp(-z)), 4)
''', [[[1, 2], [0.5, -0.25], 0], [[0, 0], [1, 1], 0], [[3], [2], -6], [[1], [4], 1]], "Weighted sum first.", approx=0.0002),
  PL("k-NN classify", "Write knn(train_X, train_y, point, k): the majority label among the k training points closest to point (squared Euclidean distance; ties in distance broken by earlier index; ties in votes go to the label that appears first among the neighbours).", "knn(train_X, train_y, point, k)", '''
def knn(train_X, train_y, point, k):
    d = []
    for i in range(len(train_X)):
        s = 0
        for j in range(len(point)):
            s = s + (train_X[i][j] - point[j]) ** 2
        d.append([s, i])
    d.sort()
    labels = [train_y[p[1]] for p in d[:k]]
    best = labels[0]
    bc = 0
    for l in labels:
        c = labels.count(l)
        if c > bc:
            bc = c
            best = l
    return best
''', [[[[0, 0], [0, 1], [5, 5], [5, 6]], ['a', 'a', 'b', 'b'], [1, 1], 3], [[[0, 0], [0, 1], [5, 5], [5, 6]], ['a', 'a', 'b', 'b'], [4, 5], 1], [[[1], [2], [3], [10]], [0, 0, 1, 1], [9], 3]], "Sort by distance, then count votes."),
  PL("Confusion counts", "Write confusion(y_true, y_pred): the list [TP, FP, FN, TN] treating label 1 as positive.", "confusion(y_true, y_pred)", '''
def confusion(y_true, y_pred):
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for i in range(len(y_true)):
        if y_pred[i] == 1 and y_true[i] == 1:
            tp = tp + 1
        elif y_pred[i] == 1 and y_true[i] == 0:
            fp = fp + 1
        elif y_pred[i] == 0 and y_true[i] == 1:
            fn = fn + 1
        else:
            tn = tn + 1
    return [tp, fp, fn, tn]
''', [[[1, 0, 1, 1, 0], [1, 0, 0, 1, 1]], [[0, 0, 0], [0, 0, 0]], [[1, 1], [0, 0]]], "Four cases."),
  PL("Precision, recall, F1", "Write prf(tp, fp, fn): the list [precision, recall, f1], each rounded to 3 decimals; a ratio with zero denominator counts as 0.", "prf(tp, fp, fn)", '''
def prf(tp, fp, fn):
    p = tp / float(tp + fp) if tp + fp > 0 else 0.0
    r = tp / float(tp + fn) if tp + fn > 0 else 0.0
    f = 2 * p * r / (p + r) if p + r > 0 else 0.0
    return [round(p, 3), round(r, 3), round(f, 3)]
''', [[2, 1, 1], [0, 0, 5], [10, 0, 0], [3, 3, 3]], "Guard against dividing by zero.", approx=0.002),
  PL("Gini impurity", "Write gini(labels): 1 minus the sum over classes of (fraction of that class) squared, rounded to 4 decimals. An empty list gives 0.", "gini(labels)", '''
def gini(labels):
    n = len(labels)
    if n == 0:
        return 0
    d = {}
    for l in labels:
        d[l] = d.get(l, 0) + 1
    s = 0.0
    for k in d:
        s = s + (d[k] / float(n)) ** 2
    return round(1 - s, 4)
''', [[['a', 'a', 'a', 'a']], [['a', 'b']], [['a', 'a', 'b', 'c']], [[]]], "Pure groups score 0.", approx=0.0002),
  PL("Best split", "Write best_threshold(values, labels): try thresholds halfway between consecutive distinct sorted values; for each, split into left (<= t) and right (> t) and compute the weighted Gini impurity; return the threshold with the lowest weighted Gini (the first one if tied), rounded to 3 decimals.", "best_threshold(values, labels)", '''
def best_threshold(values, labels):
    def g(ls):
        n = len(ls)
        if n == 0:
            return 0.0
        s = 0.0
        for k in set(ls):
            s = s + (ls.count(k) / float(n)) ** 2
        return 1 - s
    vs = sorted(set(values))
    best = None
    bt = None
    for i in range(len(vs) - 1):
        t = (vs[i] + vs[i + 1]) / 2.0
        left = [labels[j] for j in range(len(values)) if values[j] <= t]
        right = [labels[j] for j in range(len(values)) if values[j] > t]
        w = (len(left) * g(left) + len(right) * g(right)) / float(len(values))
        if best is None or w < best - 1e-9:
            best = w
            bt = t
    return round(bt, 3)
''', [[[1, 2, 3, 10, 11], ['a', 'a', 'a', 'b', 'b']], [[1, 2, 3, 4], ['a', 'b', 'b', 'b']], [[5, 1, 9, 2], [1, 0, 1, 0]]], "Scan candidate thresholds.", approx=0.002)]
))

CHS.append(CH(
 "Overfitting, validation and tuning",
 ("Validation", [
  "Overfitting | memorises | Noise",
  "Underfitting | misses | Pattern",
  "Validation set | tunes | Settings",
  "Cross-validation | averages | Several splits",
  "Hyperparameter | is | A setting you choose",
  "Grid search | tries | Combinations",
  "Baseline | sets | A bar to beat"]),
 ["A model that scores perfectly on its training data may just have memorised it. Overfitting means fitting the noise, so performance on new data is poor. Underfitting means the model is too simple to capture the pattern.",
  "To choose settings (hyperparameters) such as k in k-NN, use cross-validation: split the training data into folds, train on all but one, score on the held-out fold, and average. Keep the test set untouched until the end.",
  "Always compare against a baseline, such as predicting the mean or the most common class. A fancy model that barely beats the baseline is not worth deploying."],
 [("Overfitting", "When a model learns the training data too closely, including noise, and generalises poorly."),
  ("Underfitting", "When a model is too simple to capture the real pattern."),
  ("Cross-validation", "Estimating performance by training and scoring on several different splits and averaging."),
  ("Hyperparameter", "A setting chosen before training, such as k or tree depth, rather than learned from data."),
  ("Baseline", "A simple reference model that any useful model should beat.")],
 ["Training score high, validation low = overfit.",
  "Both low = underfit.",
  "cross_val_score(model, X, y, cv=5).",
  "GridSearchCV tries parameter combinations.",
  "Touch the test set once."],
 [T("A student who memorises last year's exam answers scores perfectly on that paper and badly on this year's. A model can do the same. Give a flexible model enough freedom, say a decision tree with no depth limit, and it will carve out a region for every training point, including the freak ones. Training accuracy hits one hundred percent, while new data tells the truth."),
  T("The telltale sign is a gap. Plot training and validation scores as complexity grows. At first both rise. Then the training score keeps rising while the validation score peaks and falls. The peak marks the sweet spot between underfitting, where the model is too rigid to see the pattern, and overfitting, where it sees patterns that are not there. This is the bias-variance trade-off."),
  T("How do we pick settings, such as the number of neighbours or the depth of a tree, without cheating? Not by looking at the test set. Instead use cross-validation. Split the training data into, say, five folds. Train on four, score on the fifth, rotate five times and average the scores. You get a more stable estimate than a single split, and the test set stays clean."),
  C("from sklearn.model_selection import cross_val_score, GridSearchCV\nfrom sklearn.neighbors import KNeighborsClassifier\n\nscores = cross_val_score(KNeighborsClassifier(5), X_train, y_train, cv=5)\nprint(scores.mean(), scores.std())\n\ngrid = GridSearchCV(KNeighborsClassifier(), {'n_neighbors': [1, 3, 5, 7, 9]}, cv=5)\ngrid.fit(X_train, y_train)\nprint(grid.best_params_, grid.score(X_test, y_test))", "python"),
  T("Last, always set a baseline. For regression, predict the training mean; for classification, predict the most common class. If your model scores barely above, the features probably carry little information, or the pipeline has a bug. Regularisation, simpler models and more data are the main cures for overfitting.")],
 [("What is overfitting?", ["Learning noise in the training data", "A model that is too simple", "A slow model", "Too much test data"], 0, "Memorising."),
  ("What does a big train-validation gap suggest?", ["Overfitting", "Underfitting", "A perfect model", "A bug in plotting"], 0, "Memorised."),
  ("What is cross-validation?", ["Averaging scores over several splits", "Scoring on the training set", "Using the test set many times", "Shuffling labels"], 0, "Folds."),
  ("What is a hyperparameter?", ["A setting chosen before training", "A learned weight", "A feature", "A label"], 0, "Like k."),
  ("Why a baseline?", ["To check that the model adds value", "To slow training", "To pick features", "To plot"], 0, "A bar to beat."),
  ("When may you use the test set?", ["Once, at the end", "For every tuning step", "Never", "During training"], 0, "Keep it clean.")],
 [("cv=5", "five folds"), ("train score - val score", "overfitting gap"), ("best_params_", "tuned settings")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Overfitting", "memorising noise"), ("Underfitting", "too simple"), ("Cross-validation", "average over folds"), ("Hyperparameter", "setting chosen before training"), ("Baseline", "simple model to beat")]),
  PL("K-fold indices", "Write kfold(n, k): split indexes 0..n-1 into k consecutive folds (the first n % k folds get one extra index); return the list of folds, each a list of indexes.", "kfold(n, k)", '''
def kfold(n, k):
    size = n // k
    extra = n % k
    folds = []
    start = 0
    for i in range(k):
        end = start + size + (1 if i < extra else 0)
        folds.append(list(range(start, end)))
        start = end
    return folds
''', [[10, 5], [7, 3], [4, 4], [5, 2]], "Spread the remainder over the first folds."),
  PL("Train and validation of fold", "Write fold_split(n, k, i): return [train_indexes, validation_indexes] where validation is fold i of kfold(n, k) and train is every other index in order.", "fold_split(n, k, i)", '''
def fold_split(n, k, i):
    size = n // k
    extra = n % k
    folds = []
    start = 0
    for f in range(k):
        end = start + size + (1 if f < extra else 0)
        folds.append(list(range(start, end)))
        start = end
    val = folds[i]
    train = [j for j in range(n) if j not in val]
    return [train, val]
''', [[6, 3, 0], [6, 3, 2], [5, 2, 0], [7, 3, 1]], "Everything not in the fold is training."),
  PL("Majority baseline", "Write majority_baseline(y_train, y_test): the accuracy (rounded to 3 decimals) of always predicting the most common training label (first seen wins ties) on y_test.", "majority_baseline(y_train, y_test)", '''
def majority_baseline(y_train, y_test):
    best = y_train[0]
    bc = 0
    for l in y_train:
        c = y_train.count(l)
        if c > bc:
            bc = c
            best = l
    hit = len([v for v in y_test if v == best])
    return round(hit / float(len(y_test)), 3)
''', [[[0, 0, 1], [0, 1, 1, 0]], [['a', 'b', 'b'], ['b', 'b', 'a', 'a']], [[1], [1, 1]]], "Predict the commonest label.", approx=0.002),
  PL("Diagnose fit", "Write diagnose(train_score, val_score): return 'overfit' if train_score - val_score > 0.1; otherwise 'underfit' if train_score < 0.7; otherwise 'good'.", "diagnose(train_score, val_score)", '''
def diagnose(train_score, val_score):
    if train_score - val_score > 0.1:
        return 'overfit'
    if train_score < 0.7:
        return 'underfit'
    return 'good'
''', [[1.0, 0.7], [0.6, 0.58], [0.9, 0.86], [0.75, 0.5]], "A simple rule of thumb."),
  PL("Grid search", "Write best_k(scores): scores is a list of [k, mean_cv_score] pairs; return the k with the highest score (the smallest k if tied).", "best_k(scores)", '''
def best_k(scores):
    best = None
    bk = None
    for pair in scores:
        k = pair[0]
        s = pair[1]
        if best is None or s > best or (s == best and k < bk):
            best = s
            bk = k
    return bk
''', [[[[1, 0.8], [3, 0.85], [5, 0.9], [7, 0.88]]], [[[1, 0.9], [3, 0.9]]], [[[9, 0.5]]]], "Prefer simpler (smaller) k on ties."),
  PL("Polynomial features", "Write poly_features(x, degree): for each value v return [v, v^2, ..., v^degree] (powers 1 to degree).", "poly_features(x, degree)", '''
def poly_features(x, degree):
    out = []
    for v in x:
        out.append([v ** p for p in range(1, degree + 1)])
    return out
''', [[[1, 2, 3], 3], [[2], 1], [[0, 1], 2]], "More powers give a more flexible model.")]
))

CHS.append(CH(
 "Unsupervised learning: clustering and PCA",
 ("Unsupervised", [
  "Clustering | groups | Similar points",
  "k-means | moves | Centres",
  "Centroid | is | Cluster mean",
  "Inertia | sums | Squared distances",
  "PCA | finds | Main directions",
  "Variance | is | Spread",
  "Dimension reduction | simplifies | Features"]),
 ["Unsupervised learning looks for structure without labels. Clustering groups similar items: customers, documents, genes. k-means alternates between assigning each point to its nearest centre and moving each centre to the mean of its points.",
  "Principal component analysis (PCA) finds the directions along which the data varies most and re-expresses the data in those directions, so that a few components may capture most of the information.",
  "Without labels, judging results is harder. Use inertia, the elbow method, and above all look at the clusters and ask whether they make sense."],
 [("Clustering", "Grouping items so that those in a group are more similar to each other than to those in other groups."),
  ("k-means", "A clustering algorithm that alternates assigning points to the nearest centroid and recomputing centroids."),
  ("Inertia", "The sum of squared distances from each point to its cluster centre."),
  ("PCA", "Principal component analysis: a rotation of the data to directions of greatest variance."),
  ("Explained variance ratio", "The fraction of total variance captured by a principal component.")],
 ["KMeans(n_clusters=3).fit(X).",
  "Assign, update, repeat until stable.",
  "Scale features first.",
  "PCA(n_components=2).fit_transform(X).",
  "Elbow: plot inertia against k."],
 [T("A shop has data on thousands of customers but no labels. Are there natural groups: bargain hunters, loyal regulars, big spenders? Clustering looks for them. It finds groups, but it cannot name them. That is your job."),
  T("k-means is the classic algorithm. Pick k, the number of clusters, and place k centres at random. Then repeat two steps. First, assign every point to its nearest centre. Second, move each centre to the mean of the points assigned to it. Stop when nothing changes. Each round reduces the inertia, the total squared distance of points to their centres."),
  C("from sklearn.cluster import KMeans\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.decomposition import PCA\n\nXs = StandardScaler().fit_transform(X)\nfor k in range(1, 8):\n    print(k, KMeans(n_clusters=k, n_init=10).fit(Xs).inertia_)\nkm = KMeans(n_clusters=3, n_init=10).fit(Xs)\nlabels = km.labels_\nXp = PCA(n_components=2).fit_transform(Xs)", "python"),
  T("How many clusters? Plot the inertia for different k. It always falls as k grows, but where the drop slows sharply, the elbow, is a reasonable choice. Distances drive k-means, so scale the features first, or a column in large units will decide everything. It also assumes roundish clusters of similar size and can land in poor local optima, so run it several times."),
  T("Many datasets have dozens of features, but the interesting variation lies along a few directions. PCA finds the direction of greatest spread, then the next, perpendicular to it, and so on. Keeping the first two or three gives a picture you can plot and a compact input for other models. The ratio of variance each component explains tells you how much you lose.")],
 [("What does k-means alternate between?", ["Assigning points and moving centres", "Sorting and merging", "Fitting and predicting", "Scaling and encoding"], 0, "Two steps."),
  ("What is a centroid?", ["The mean of a cluster's points", "The first point", "The largest point", "A label"], 0, "Cluster centre."),
  ("What is the elbow method?", ["Choose k where inertia falls slowly", "Choose k = 2", "Pick the smallest inertia", "Use a plot of labels"], 0, "Diminishing returns."),
  ("Why scale before k-means?", ["Distances depend on units", "To add labels", "To add noise", "To sort"], 0, "Large units dominate."),
  ("What does PCA find?", ["Directions of greatest variance", "Clusters", "Labels", "Outliers only"], 0, "Principal components."),
  ("Do clusters come with names?", ["No, you interpret them", "Yes", "Only in k-means", "Only in PCA"], 0, "Unsupervised.")],
 [("inertia = sum |x - c|^2", "k-means objective"), ("PCA(n_components=2)", "reduce to 2 dims"), ("explained_variance_ratio_", "information kept")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("k-means", "assign then recentre"), ("Centroid", "mean of a cluster"), ("Inertia", "sum of squared distances"), ("PCA", "directions of greatest variance"), ("Elbow", "where improvement slows")]),
  PL("Assign to nearest", "Write assign(points, centres): for each point (a list of numbers) the index of the nearest centre by squared distance (the lowest index on ties).", "assign(points, centres)", '''
def assign(points, centres):
    out = []
    for p in points:
        best = 0
        bd = None
        for i in range(len(centres)):
            d = 0
            for j in range(len(p)):
                d = d + (p[j] - centres[i][j]) ** 2
            if bd is None or d < bd:
                bd = d
                best = i
        out.append(best)
    return out
''', [[[[0, 0], [1, 1], [9, 9], [10, 10]], [[0, 0], [10, 10]]], [[[5, 5]], [[0, 0], [10, 10]]], [[[1], [4], [6]], [[2], [5]]]], "Compare squared distances."),
  PL("Update centres", "Write update(points, labels, k): the mean of the points of each cluster 0..k-1 as lists, rounded to 2 decimals; a cluster with no points gets the list of zeros.", "update(points, labels, k)", '''
def update(points, labels, k):
    d = len(points[0])
    out = []
    for c in range(k):
        members = [points[i] for i in range(len(points)) if labels[i] == c]
        if len(members) == 0:
            out.append([0] * d)
        else:
            out.append([round(sum([m[j] for m in members]) / float(len(members)), 2) for j in range(d)])
    return out
''', [[[[0, 0], [2, 2], [10, 10], [12, 14]], [0, 0, 1, 1], 2], [[[1], [3]], [0, 0], 2], [[[1, 1]], [0], 1]], "Average the members."),
  PL("Inertia", "Write inertia(points, centres, labels): the sum of squared distances from each point to the centre of its label, rounded to 2 decimals.", "inertia(points, centres, labels)", '''
def inertia(points, centres, labels):
    s = 0.0
    for i in range(len(points)):
        c = centres[labels[i]]
        for j in range(len(c)):
            s = s + (points[i][j] - c[j]) ** 2
    return round(s, 2)
''', [[[[0, 0], [2, 2], [10, 10]], [[1, 1], [10, 10]], [0, 0, 1]], [[[1], [3]], [[2]], [0, 0]], [[[5]], [[5]], [0]]], "Sum squared distances.", approx=0.01),
  PL("k-means", "Write kmeans(points, centres, iterations): run the assign and update steps iterations times starting from the given centres (an empty cluster keeps its old centre) and return [labels, centres] with centres rounded to 2 decimals.", "kmeans(points, centres, iterations)", '''
def kmeans(points, centres, iterations):
    centres = [list(c) for c in centres]
    labels = []
    for it in range(iterations):
        labels = []
        for p in points:
            best = 0
            bd = None
            for i in range(len(centres)):
                d = 0
                for j in range(len(p)):
                    d = d + (p[j] - centres[i][j]) ** 2
                if bd is None or d < bd:
                    bd = d
                    best = i
            labels.append(best)
        new = []
        for c in range(len(centres)):
            members = [points[i] for i in range(len(points)) if labels[i] == c]
            if len(members) == 0:
                new.append(centres[c])
            else:
                new.append([round(sum([m[j] for m in members]) / float(len(members)), 2) for j in range(len(centres[c]))])
        centres = new
    return [labels, centres]
''', [[[[0, 0], [1, 0], [9, 9], [10, 9]], [[0, 0], [5, 5]], 3], [[[1], [2], [8], [9], [10]], [[1], [2]], 4], [[[0, 0], [4, 4]], [[0, 0], [4, 4]], 2]], "Alternate until the iterations end."),
  PL("Variance explained", "Write var_explained(x, y): for 2D data given as two equal-length lists, return the fraction of total variance along the x axis: var(x) / (var(x) + var(y)), rounded to 3 decimals (population variance).", "var_explained(x, y)", '''
def var_explained(x, y):
    def v(a):
        m = sum(a) / float(len(a))
        return sum([(t - m) ** 2 for t in a]) / float(len(a))
    return round(v(x) / (v(x) + v(y)), 3)
''', [[[1, 2, 3, 4], [5, 5, 5, 5]], [[1, 2, 3], [1, 2, 3]], [[0, 10], [0, 1]]], "Compare the two variances.", approx=0.002),
  PL("Covariance", "Write covariance(x, y): the population covariance of two lists, rounded to 3 decimals (this is the off-diagonal entry that PCA uses).", "covariance(x, y)", '''
def covariance(x, y):
    n = len(x)
    mx = sum(x) / float(n)
    my = sum(y) / float(n)
    return round(sum([(x[i] - mx) * (y[i] - my) for i in range(n)]) / n, 3)
''', [[[1, 2, 3], [2, 4, 6]], [[1, 2, 3], [3, 2, 1]], [[1, 2], [5, 5]]], "Average product of deviations.", approx=0.002)]
))

CHS.append(CH(
 "Neural networks and Keras",
 ("Neural networks", [
  "Neuron | computes | Weighted sum",
  "Activation | adds | Non-linearity",
  "Layer | holds | Many neurons",
  "Loss | measures | Error",
  "Backpropagation | computes | Gradients",
  "Epoch | is | One pass of data",
  "Keras | builds | Networks easily"]),
 ["A neuron computes a weighted sum of its inputs plus a bias and passes it through an activation function. A layer is many neurons side by side, and a network stacks layers. Without non-linear activations such as ReLU, a stack of layers would collapse into one linear model.",
  "Training adjusts the weights to reduce a loss, using gradient descent. Backpropagation applies the chain rule to find how the loss changes with every weight. One full pass over the training data is an epoch.",
  "Keras lets you describe a network in a few lines: a Sequential model of Dense layers, compile with a loss and optimiser, then fit. The key risk is overfitting, so watch validation loss."],
 [("Neuron", "A unit that computes activation(w . x + b)."),
  ("Activation function", "A non-linear function applied to a neuron's sum, such as ReLU, sigmoid or softmax."),
  ("Loss function", "A number measuring how wrong the predictions are, which training tries to minimise."),
  ("Backpropagation", "An algorithm that computes the gradient of the loss with respect to every weight using the chain rule."),
  ("Epoch", "One complete pass through the training data.")],
 ["Dense(16, activation='relu').",
  "model.compile(optimizer='adam', loss='...').",
  "model.fit(X, y, epochs=20, validation_split=0.2).",
  "ReLU(z) = max(0, z).",
  "Softmax turns scores into probabilities."],
 [T("A neural network is a stack of layers of simple units. Each neuron takes its inputs, multiplies each by a weight, adds them with a bias and applies an activation function. A single neuron with a sigmoid activation is exactly logistic regression. The power comes from stacking."),
  T("Why do we need the activation? Stacking linear steps gives just another linear step, so depth would add nothing. A non-linear activation such as the rectified linear unit, ReLU, which outputs zero for negative inputs and the input itself otherwise, lets the network bend. The classic example is XOR, which no single linear boundary can separate, but a layer of two hidden neurons can."),
  C("from tensorflow import keras\nfrom tensorflow.keras import layers\n\nmodel = keras.Sequential([\n    layers.Input(shape=(4,)),\n    layers.Dense(16, activation='relu'),\n    layers.Dense(8, activation='relu'),\n    layers.Dense(3, activation='softmax'),\n])\nmodel.compile(optimizer='adam',\n              loss='sparse_categorical_crossentropy',\n              metrics=['accuracy'])\nhistory = model.fit(X_train, y_train, epochs=30, batch_size=32,\n                    validation_split=0.2)\nmodel.evaluate(X_test, y_test)", "python"),
  T("Read that code as a recipe. Sequential stacks layers. Dense means every neuron connects to every input. The last layer has one neuron per class with softmax, which turns raw scores into probabilities that sum to one. Compile chooses a loss, here cross-entropy, which punishes confident wrong answers, and an optimiser, Adam, a clever gradient descent. Fit then loops over the data for a number of epochs."),
  T("Where do the gradients come from? Backpropagation. The forward pass computes predictions and the loss. The backward pass uses the chain rule to push the error back through each layer, giving the gradient of the loss with respect to every weight. Libraries do this automatically, so you only describe the forward computation."),
  T("Neural networks shine on images, text and audio, where there are huge datasets and no good hand-made features. For small tables, simpler models such as gradient-boosted trees often win. Use the playground to train a tiny network on a spiral, change the hidden units and the learning rate, and watch the boundary bend into shape.")],
 [("What does a neuron compute?", ["Activation of weighted sum plus bias", "A random number", "The mean of a column", "A distance"], 0, "w.x + b."),
  ("Why use activation functions?", ["To add non-linearity", "To save memory", "To sort data", "To scale labels"], 0, "Otherwise linear."),
  ("What does softmax produce?", ["Probabilities that sum to 1", "A single number", "A label", "A distance"], 0, "Last layer."),
  ("What is an epoch?", ["One pass through the training data", "One neuron", "One layer", "One batch"], 0, "Training loop."),
  ("What does backpropagation compute?", ["Gradients of the loss", "Predictions", "Labels", "Features"], 0, "Chain rule."),
  ("What does compile choose?", ["Loss and optimiser", "The data", "The weights", "The labels"], 0, "Before fit.")],
 [("ReLU(z) = max(0, z)", "rectified linear unit"), ("softmax(z)_i = e^z_i / sum e^z", "class probabilities"), ("w = w - lr x grad", "weight update")],
 [APP("NN", "Neural network playground", "Train a small network on 2D data. Choose a dataset (circle, XOR or spiral), the hidden units and the learning rate, press Train, and watch the loss fall and the boundary bend. Reach 95 percent accuracy on any dataset to complete the lab.", 820),
  MATCH("Match the term", "Pair each term with its meaning.", [("Neuron", "weighted sum then activation"), ("ReLU", "max of zero and input"), ("Softmax", "scores to probabilities"), ("Loss", "number to minimise"), ("Epoch", "one pass over the data")]),
  PL("ReLU", "Write relu_list(x): apply max(0, v) to each element of a list.", "relu_list(x)", '''
def relu_list(x):
    return [v if v > 0 else 0 for v in x]
''', [[[-1, 0, 2, -3.5, 4]], [[1, 2]], [[-5]]], "Zero for negatives."),
  PL("Softmax", "Write softmax(z): the softmax of a list, e^z_i / sum of e^z_j, each rounded to 4 decimals.", "softmax(z)", '''
import math
def softmax(z):
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [round(v / s, 4) for v in e]
''', [[[1, 2, 3]], [[0, 0]], [[10, 0]], [[-1, 1]]], "Subtract the max for stability.", approx=None),
  PL("One neuron", "Write neuron(x, w, b, act): activation of w.x + b where act is 'relu', 'sigmoid' or 'linear'. Round to 4 decimals.", "neuron(x, w, b, act)", '''
import math
def neuron(x, w, b, act):
    z = b
    for i in range(len(w)):
        z = z + w[i] * x[i]
    if act == 'relu':
        z = max(0, z)
    elif act == 'sigmoid':
        z = 1.0 / (1.0 + math.exp(-z))
    return round(z, 4)
''', [[[1, 2], [0.5, -1], 0.5, 'relu'], [[1, 2], [0.5, -1], 0.5, 'sigmoid'], [[3], [2], 1, 'linear'], [[0, 0], [1, 1], -1, 'relu']], "Weighted sum then activation.", approx=0.0002),
  PL("Solve XOR", "XOR needs a hidden layer. Write xor_net(a, b) for a, b in {0, 1}: hidden neurons h1 = relu(a + b) and h2 = relu(a + b - 1), output = h1 - 2 x h2. Return the output as an integer.", "xor_net(a, b)", '''
def xor_net(a, b):
    h1 = max(0, a + b)
    h2 = max(0, a + b - 1)
    return h1 - 2 * h2
''', [[0, 0], [0, 1], [1, 0], [1, 1]], "Two ReLU units can make the fold."),
  PL("Forward pass", "Write forward(x, layers): layers is a list of [W, b] where W is a list of rows (one per neuron) and b a list of biases; every layer uses ReLU except the last, which is linear. Return the final output list rounded to 3 decimals.", "forward(x, layers)", '''
def forward(x, layers):
    a = list(x)
    for li in range(len(layers)):
        W = layers[li][0]
        b = layers[li][1]
        out = []
        for i in range(len(W)):
            s = b[i]
            for j in range(len(a)):
                s = s + W[i][j] * a[j]
            if li < len(layers) - 1:
                s = max(0, s)
            out.append(s)
        a = out
    return [round(v, 3) for v in a]
''', [[[1, 2], [[[[1, 1], [1, -1]], [0, 0]], [[[1, 1]], [0]]]], [[0, 0], [[[[1, 1], [1, -1]], [0, 1]], [[[2, 3]], [0.5]]]], [[1], [[[[2]], [-1]]]]], "Loop over layers; skip ReLU on the last."),
  PL("Cross-entropy", "Write cross_entropy(probs, true_index): the loss -ln(probs[true_index]), rounded to 4 decimals.", "cross_entropy(probs, true_index)", '''
import math
def cross_entropy(probs, true_index):
    return round(-math.log(probs[true_index]), 4)
''', [[[0.7, 0.2, 0.1], 0], [[0.7, 0.2, 0.1], 2], [[0.5, 0.5], 1], [[1.0, 0.0], 0]], "Confident wrong answers cost a lot.", approx=0.0002),
  PL("One training step", "Train a single sigmoid neuron on one example with squared error: p = sigmoid(w x + b); error = p - y; w_new = w - lr x error x p x (1 - p) x x; b_new = b - lr x error x p x (1 - p). Write step(w, b, x, y, lr) returning [w_new, b_new] rounded to 4 decimals.", "step(w, b, x, y, lr)", '''
import math
def step(w, b, x, y, lr):
    p = 1.0 / (1.0 + math.exp(-(w * x + b)))
    g = (p - y) * p * (1 - p)
    return [round(w - lr * g * x, 4), round(b - lr * g, 4)]
''', [[0, 0, 1, 1, 1], [1, 0, 2, 0, 0.5], [-1, 1, 1, 1, 2]], "Chain rule through the sigmoid.", approx=None)]
))

CHS.append(CH(
 "Putting it together: projects, ethics and next steps",
 ("Practice", [
  "Project | follows | The workflow",
  "Baseline | comes | First",
  "Leakage | must be | Avoided",
  "Bias | can enter | Through data",
  "Fairness | needs | Group checks",
  "Reproducibility | needs | Seeds and versions",
  "Communication | closes | The loop"]),
 ["A good project starts with a clear question and a baseline, builds a simple model, adds complexity only when validation shows it helps, and reports results with honest uncertainty. Keep random seeds and package versions so others can repeat the work.",
  "Models learn from the data they are given, including its biases. Check performance for different groups, ask who might be harmed by errors, and be open about limits.",
  "From here: practise on real datasets, learn more statistics, try gradient boosting, deep learning for images and text, and deploy a small model."],
 [("Reproducibility", "Being able to rerun an analysis and get the same results, using fixed seeds, recorded versions and clean code."),
  ("Bias (fairness sense)", "Systematic unfairness in data or model outputs that disadvantages some groups."),
  ("Selection rate", "The fraction of a group that receives a positive prediction."),
  ("Model card", "A short document describing a model's purpose, data, performance and limits."),
  ("Deployment", "Putting a trained model to work on new data in a real system.")],
 ["Question, baseline, simple model, validate, improve.",
  "Split before anything else.",
  "Check subgroups, not only the average.",
  "Set random_state; record versions.",
  "Explain results to non-experts."],
 [T("Let us rehearse a whole project in prose. A clinic wants to predict missed appointments. First the question: who is likely to miss, so that we can send a reminder? Then the data: past appointments with date, age group, distance, previous misses and whether the patient came. Split off a test set immediately and lock it away."),
  T("Explore with pandas and Matplotlib: how many appointments are missed overall, how it varies by weekday, by distance. Fix or flag odd values. Build a baseline that always predicts attend: it is right about eighty percent of the time. Any model must beat that on recall of the missed class, because that is what the clinic cares about."),
  C("from sklearn.pipeline import Pipeline\nfrom sklearn.compose import ColumnTransformer\nfrom sklearn.preprocessing import OneHotEncoder, StandardScaler\nfrom sklearn.ensemble import RandomForestClassifier\n\nprep = ColumnTransformer([\n    ('num', StandardScaler(), ['age', 'distance', 'prev_missed']),\n    ('cat', OneHotEncoder(handle_unknown='ignore'), ['weekday']),\n])\nclf = Pipeline([('prep', prep), ('model', RandomForestClassifier(random_state=0))])\nclf.fit(X_train, y_train)\nprint(clf.score(X_test, y_test))", "python"),
  T("Next, fairness. Suppose the model flags patients from one neighbourhood twice as often as others. Is that because they really miss more, perhaps from poor bus links, or because the training data under-represents them? Compare the selection rate and the error rates by group. A model can have good average accuracy and still treat a group badly. Decide in advance which disparities you will accept, and explain."),
  T("Finally, reproducibility and communication. Set random seeds, record library versions, keep the code in version control and write a short model card: what the model is for, what data it saw, how well it works, where it fails. Present results with plain words and honest uncertainty. A model nobody trusts or understands will not be used.")],
 [("What should come right after defining the question?", ["Collecting data and a split", "Deploying", "Tuning hyperparameters", "Writing the report"], 0, "Lock away the test set."),
  ("Why use a baseline?", ["To check the model adds value", "To look professional", "To avoid data", "To speed training"], 0, "A bar to beat."),
  ("What is a selection rate?", ["Fraction of a group predicted positive", "Fraction of accurate predictions", "A random seed", "A score"], 0, "Per group."),
  ("Why set random seeds?", ["For reproducibility", "To make the model smarter", "To speed training", "To hide errors"], 0, "Same results."),
  ("What is a model card?", ["A short description of purpose and limits", "A credit card", "A plot", "A data table"], 0, "Transparency."),
  ("Can average accuracy hide unfair results?", ["Yes", "No", "Only for trees", "Only for neural nets"], 0, "Check subgroups.")],
 [("random_state=0", "reproducible split or model"), ("selection rate", "positives per group"), ("model card", "documentation of a model")],
 [ORDER("A sound project order", "Put these project steps in a sensible order.", ["Define the question", "Split off the test set", "Explore and clean the training data", "Build a baseline", "Train and tune models with cross-validation", "Evaluate once on the test set", "Report with limits and fairness checks"]),
  MATCH("Match the practice", "Pair each practice with its aim.", [("Baseline", "check the model adds value"), ("Seeds and versions", "reproducibility"), ("Group metrics", "spot unfair errors"), ("Model card", "explain purpose and limits"), ("Held-out test set", "honest final score")]),
  PL("Group selection rates", "Write selection_rates(groups, preds): the fraction of predictions equal to 1 for each distinct group, as a list of [group, rate] pairs sorted by group, rates rounded to 3 decimals.", "selection_rates(groups, preds)", '''
def selection_rates(groups, preds):
    tot = {}
    pos = {}
    for i in range(len(groups)):
        g = groups[i]
        tot[g] = tot.get(g, 0) + 1
        if preds[i] == 1:
            pos[g] = pos.get(g, 0) + 1
    out = []
    for g in sorted(tot.keys()):
        out.append([g, round(pos.get(g, 0) / float(tot[g]), 3)])
    return out
''', [[['a', 'a', 'b', 'b', 'b'], [1, 0, 1, 1, 0]], [['x', 'x'], [0, 0]], [['p', 'q'], [1, 1]]], "Count positives and totals per group.", approx=None),
  PL("Disparity ratio", "Write disparity(rates): rates is a list of [group, rate]; return the ratio of the lowest rate to the highest, rounded to 3 decimals (1.0 if the highest is 0).", "disparity(rates)", '''
def disparity(rates):
    vals = [r[1] for r in rates]
    hi = max(vals)
    if hi == 0:
        return 1.0
    return round(min(vals) / hi, 3)
''', [[[['a', 0.5], ['b', 0.25]]], [[['a', 0.4], ['b', 0.4]]], [[['a', 0], ['b', 0]]]], "Lowest over highest.", approx=0.002),
  PL("Leakage check", "Write leakage(train_ids, test_ids): the sorted list of ids that appear in both lists (a sign of leakage).", "leakage(train_ids, test_ids)", '''
def leakage(train_ids, test_ids):
    return sorted(list(set(train_ids) & set(test_ids)))
''', [[[1, 2, 3], [3, 4, 5]], [[1, 2], [3, 4]], [[7, 7, 8], [7]]], "Intersect the sets."),
  PL("Recall for the missed class", "Write recall_for(y_true, y_pred, label): of the cases whose true label equals label, the fraction predicted as label, rounded to 3 decimals (0 if there are none).", "recall_for(y_true, y_pred, label)", '''
def recall_for(y_true, y_pred, label):
    n = 0
    hit = 0
    for i in range(len(y_true)):
        if y_true[i] == label:
            n = n + 1
            if y_pred[i] == label:
                hit = hit + 1
    if n == 0:
        return 0
    return round(hit / float(n), 3)
''', [[['miss', 'ok', 'miss', 'ok'], ['ok', 'ok', 'miss', 'ok'], 'miss'], [['ok', 'ok'], ['ok', 'ok'], 'miss'], [['a', 'a'], ['a', 'a'], 'a']], "Only look at cases of that label.", approx=0.002),
  PL("Model summary", "Write summarise(name, train_score, test_score, baseline): return a one-line string 'NAME: train T, test S, baseline B, beats baseline: yes/no' with scores shown with exactly 2 decimals (format with '%.2f'), yes if test_score > baseline.", "summarise(name, train_score, test_score, baseline)", '''
def summarise(name, train_score, test_score, baseline):
    def f(v):
        return '%.2f' % v
    verdict = 'yes' if test_score > baseline else 'no'
    return name + ': train ' + f(train_score) + ', test ' + f(test_score) + ', baseline ' + f(baseline) + ', beats baseline: ' + verdict
''', [['knn', 0.9, 0.85, 0.8], ['tree', 1.0, 0.7, 0.8], ['reg', 0.5, 0.5, 0.45]], "Build the string piece by piece.")]
))
