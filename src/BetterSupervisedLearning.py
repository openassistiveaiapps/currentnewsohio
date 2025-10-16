# ============================================
# 🤖 Rule-based vs ML vs Feature-Engineered ML
# Author: AI Classroom Demo
# ============================================

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# ------------------------------------------------
# 🧮 1. RULE-BASED APPROACH — Deterministic Logic
# ------------------------------------------------
def rule_based_odd_even(numbers):
    results = []
    for num in numbers:
        label = "Even" if num % 2 == 0 else "Odd"
        results.append(label)
    return results


# ------------------------------------------------
# 🧠 2. LOGISTIC REGRESSION (Naive)
# ------------------------------------------------
def logistic_regression_naive(train_numbers, test_numbers):
    X_train = np.array([[n] for n in train_numbers])
    y_train = np.array([0 if n % 2 else 1 for n in train_numbers])

    model = LogisticRegression()
    model.fit(X_train, y_train)

    X_test = np.array([[n] for n in test_numbers])
    preds = model.predict(X_test)
    return ["Even" if p == 1 else "Odd" for p in preds]


# ------------------------------------------------
# 🧠 3. LOGISTIC REGRESSION (with Feature Engineering)
# ------------------------------------------------
def logistic_regression_mod_feature(train_numbers, test_numbers):
    X_train = np.array([[n % 2] for n in train_numbers])
    y_train = np.array([0 if n % 2 else 1 for n in train_numbers])

    model = LogisticRegression()
    model.fit(X_train, y_train)

    X_test = np.array([[n % 2] for n in test_numbers])
    preds = model.predict(X_test)
    return ["Even" if p == 1 else "Odd" for p in preds]


# ------------------------------------------------
# 🌳 4. DECISION TREE (Naive vs Feature Engineered)
# ------------------------------------------------
def decision_tree_naive(train_numbers, test_numbers):
    X_train = np.array([[n] for n in train_numbers])
    y_train = np.array([0 if n % 2 else 1 for n in train_numbers])

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    X_test = np.array([[n] for n in test_numbers])
    preds = model.predict(X_test)
    return ["Even" if p == 1 else "Odd" for p in preds]


def decision_tree_mod_feature(train_numbers, test_numbers):
    X_train = np.array([[n % 2] for n in train_numbers])
    y_train = np.array([0 if n % 2 else 1 for n in train_numbers])

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    X_test = np.array([[n % 2] for n in test_numbers])
    preds = model.predict(X_test)
    return ["Even" if p == 1 else "Odd" for p in preds]


# ------------------------------------------------
# 🧪 DEMO RUN
# ------------------------------------------------
if __name__ == "__main__":
    train_numbers = list(range(1, 21))
    test_numbers = [21, 22, 23, 24]

    print("\n==========================")
    print(" RULE-BASED SYSTEM")
    print("==========================")
    rb_results = rule_based_odd_even(test_numbers)
    for n, r in zip(test_numbers, rb_results):
        print(f"{n} ➝ {r}")

    print("\n==========================")
    print(" LOGISTIC REGRESSION (Naive)")
    print("==========================")
    lr_naive = logistic_regression_naive(train_numbers, test_numbers)
    for n, r in zip(test_numbers, lr_naive):
        print(f"{n} ➝ {r}")

    print("\n==========================")
    print(" LOGISTIC REGRESSION (Mod Feature)")
    print("==========================")
    lr_mod = logistic_regression_mod_feature(train_numbers, test_numbers)
    for n, r in zip(test_numbers, lr_mod):
        print(f"{n} ➝ {r}")

    print("\n==========================")
    print(" DECISION TREE (Naive)")
    print("==========================")
    dt_naive = decision_tree_naive(train_numbers, test_numbers)
    for n, r in zip(test_numbers, dt_naive):
        print(f"{n} ➝ {r}")

    print("\n==========================")
    print(" DECISION TREE (Mod Feature)")
    print("==========================")
    dt_mod = decision_tree_mod_feature(train_numbers, test_numbers)
    for n, r in zip(test_numbers, dt_mod):
        print(f"{n} ➝ {r}")
