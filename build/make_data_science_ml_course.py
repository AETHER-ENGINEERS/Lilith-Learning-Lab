#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Data Science and ML course. Usage: python3 make_data_science_ml_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "dsml"))
import cmk, ds_a, ds_b, make_apps  # noqa: E402
make_apps.main()
CHS = ds_a.CHS + ds_b.CHS
PRONOUNCE = {"NumPy": "num pie", "pandas": "pandas", "Matplotlib": "mat plot lib", "scikit-learn": "sigh kit learn", "sklearn": "sigh kit learn", "Keras": "keh rass", "TensorFlow": "tensor flow",
    "DataFrame": "data frame", "DataFrames": "data frames", "Series": "series", "NaN": "nan", "ndarray": "en d array", "ReLU": "rel you", "softmax": "soft max", "sigmoid": "sig moid",
    "logistic": "low jis tik", "k-NN": "K N N", "k-means": "K means", "PCA": "P C A", "EDA": "E D A", "MSE": "M S E", "F1": "F one", "Gini": "jee nee", "hyperparameter": "hyper parameter",
    "hyperparameters": "hyper parameters", "Adam": "adam", "tanh": "tanch", "XOR": "ex or", "epoch": "ee pock", "epochs": "ee pocks", "overfitting": "over fitting", "underfitting": "under fitting",
    "numpy": "num pie", "np": "N P", "plt": "P L T", "pd": "P D", "csv": "C S V", "CSV": "C S V"}
SANDBOX = cmk.terminal("Data science cheat sheet", "ds>", "A scripted lookup. Try: numpy, pandas, plot, split, fit, metrics, cv, kmeans, keras", [
    ("numpy", ["a = np.array([...]); a.shape; a.mean(axis=0); a @ b; a[a > 0]."]),
    ("pandas", ["df = pd.read_csv(f); df.head(); df[df.x > 1]; df.groupby('k')['v'].mean(); df.fillna(df.median())."]),
    ("plot", ["plt.scatter(x, y); plt.hist(x, bins=20); plt.xlabel('...'); plt.show()."]),
    ("split", ["X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0). Fit scalers on train only."]),
    ("fit", ["model = LinearRegression().fit(X_tr, y_tr); model.predict(X_te); model.score(X_te, y_te)."]),
    ("metrics", ["precision = TP/(TP+FP); recall = TP/(TP+FN); F1 = 2PR/(P+R); MSE = mean((y - y_hat)^2)."]),
    ("cv", ["cross_val_score(model, X, y, cv=5); GridSearchCV(model, params, cv=5)."]),
    ("kmeans", ["KMeans(n_clusters=3, n_init=10).fit(X_scaled); inertia_ and the elbow method."]),
    ("keras", ["Sequential([Dense(16, 'relu'), Dense(3, 'softmax')]); compile(optimizer='adam', loss=...); fit(X, y, epochs=30)."]),
])
EXAM = [
 ("What is a feature?", ["An input variable used for prediction", "The thing predicted", "A plot", "A file"], 0, "A column of X."),
 ("Which task predicts a number?", ["Regression", "Classification", "Clustering", "Encoding"], 0, "House price."),
 ("What is unsupervised learning?", ["Finding structure without labels", "Learning with answers", "Learning by reward", "Memorising"], 0, "Clusters."),
 ("What does NumPy provide?", ["Fast arrays", "Tables with labels", "Neural networks", "Charts"], 0, "ndarray."),
 ("What does a.mean(axis=0) return?", ["The mean of each column", "The mean of each row", "One overall mean", "The shape"], 0, "Down the rows."),
 ("What is broadcasting?", ["Stretching small arrays to fit larger ones", "Printing arrays", "Sorting arrays", "Copying arrays"], 0, "Shape rules."),
 ("What is a pandas Series?", ["One labelled column", "A whole table", "A model", "A chart"], 0, "1D."),
 ("What does groupby do?", ["Split, apply, combine", "Sort a list", "Delete rows", "Plot"], 0, "Per group."),
 ("Which chart shows a distribution?", ["Histogram", "Line plot", "Scatter plot", "Table"], 0, "Counts per bin."),
 ("What does correlation of -1 mean?", ["Perfect opposite linear movement", "No link", "Perfect together", "Error"], 0, "Straight downhill."),
 ("What does one-hot encoding do?", ["A 0/1 column per category", "Scales a column", "Fills gaps", "Splits data"], 0, "Indicators."),
 ("Where must a scaler be fitted?", ["On training data only", "On all data", "On the test set", "Nowhere"], 0, "Avoid leakage."),
 ("What is data leakage?", ["Test information influencing training", "Losing a file", "A slow model", "Too many columns"], 0, "Too-good scores."),
 ("What does least squares minimise?", ["The sum of squared errors", "The sum of errors", "The slope", "The intercept"], 0, "Squared."),
 ("What does R squared of 1 mean?", ["A perfect fit", "No fit", "An error", "A baseline"], 0, "All variation explained."),
 ("What does sigmoid output?", ["A number between 0 and 1", "Any number", "A label", "A distance"], 0, "Probability."),
 ("How does k-NN classify?", ["Vote of the nearest points", "A formula", "Random choice", "Sorting"], 0, "Neighbours."),
 ("What is recall?", ["Fraction of real positives found", "Fraction of alarms right", "Accuracy", "Threshold"], 0, "TP / (TP + FN)."),
 ("Why is accuracy misleading?", ["With imbalanced classes", "It is slow", "It needs labels", "It is always wrong"], 0, "Always say healthy."),
 ("What is overfitting?", ["Learning noise in the training data", "A too-simple model", "A slow model", "Too much test data"], 0, "Memorising."),
 ("What is cross-validation?", ["Averaging scores over several splits", "Scoring on training data", "Using the test set repeatedly", "Shuffling labels"], 0, "Folds."),
 ("What is a hyperparameter?", ["A setting chosen before training", "A learned weight", "A label", "A feature"], 0, "Like k."),
 ("What does k-means alternate between?", ["Assigning points and moving centres", "Sorting and merging", "Fitting and predicting", "Scaling and encoding"], 0, "Two steps."),
 ("What does PCA find?", ["Directions of greatest variance", "Clusters", "Labels", "Outliers"], 0, "Principal components."),
 ("Why use an activation function?", ["To add non-linearity", "To save memory", "To sort data", "To scale labels"], 0, "Otherwise just linear."),
 ("What does softmax produce?", ["Probabilities that sum to 1", "One number", "A label", "A distance"], 0, "Last layer."),
 ("What does model.compile choose in Keras?", ["Loss and optimiser", "The data", "The labels", "The weights"], 0, "Before fit."),
 ("What is an epoch?", ["One pass through the training data", "One neuron", "One layer", "One batch"], 0, "Training loop."),
 ("Why check groups separately?", ["Average accuracy can hide unfair errors", "To slow training", "To add features", "To plot more"], 0, "Fairness."),
]
CFG = dict(id="data-science-ml", title="Data Science and Machine Learning",
    subtitle="NumPy, pandas, Matplotlib, scikit-learn and Keras from first principles, with Python labs and four interactive playgrounds",
    description="A first course in data science and machine learning in the order you meet the tools: the data science workflow; NumPy arrays and vectorised thinking; pandas tables, filtering, groupby, missing data and merging; Matplotlib and exploratory data analysis; preparing data with encoding, scaling and train-test splits; linear regression and the scikit-learn estimator pattern; classification with logistic regression, k-nearest neighbours, decision trees and precision and recall; overfitting, cross-validation and tuning; clustering with k-means and PCA; neural networks and Keras; and a project workflow with fairness checks. Lessons show real library code; the Python labs rebuild each idea in plain Python so you understand what the libraries do. Four live labs let you explore plots, regression, k-NN boundaries and train a small neural network.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="dsml", apps={"__PLOT__": "plot.html", "__REG__": "reg.html", "__KNN__": "knn.html", "__NN__": "nn.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "data-science-ml.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
