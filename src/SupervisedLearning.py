from sklearn.linear_model import LogisticRegression
import numpy as np

# ---- Training data ----
# X = numbers, y = labels (0 = Odd, 1 = Even)
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
y = np.array([0, 1, 0, 1, 0, 1, 0, 1])

# ---- Train model ----
model = LogisticRegression()
model.fit(X, y)

# ---- Predict ----
test_numbers = np.array([[9], [10], [11], [12]])
predictions = model.predict(test_numbers)

for num, pred in zip(test_numbers.flatten(), predictions):
    label = "Even" if pred == 1 else "Odd"
    print(f"{num} ➝ {label}")
