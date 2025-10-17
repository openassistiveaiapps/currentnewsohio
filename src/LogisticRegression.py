import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Sample data: numbers from 0 to 9
X = np.arange(0, 10).reshape(-1, 1)   # Features (0,1,2,...9)
y = np.array([0 if i % 2 == 0 else 1 for i in X.flatten()])  # Labels: 0 = even, 1 = odd

# Split train & test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)

print("Test labels:", y_test)
print("Predicted labels:", y_pred)
print("Predicted probabilities:\n", y_prob)

# Plot the sigmoid curve
x_range = np.linspace(-1, 10, 200).reshape(-1, 1)
y_sigmoid = model.predict_proba(x_range)[:, 1]  # Probability of class '1' (odd)

plt.figure(figsize=(8, 5))
plt.scatter(X_train, y_train, c='blue', label='Train Data', marker='o')
plt.scatter(X_test, y_test, c='red', label='Test Data', marker='x')  # Black cross here 🔸
plt.plot(x_range, y_sigmoid, color='black', label='Sigmoid Curve')
plt.axhline(0.5, color='gray', linestyle='--', label='Decision Boundary (0.5)')
plt.xlabel('Number')
plt.ylabel('Probability (Odd)')
plt.legend()
plt.show()



# numpy → for numerical arrays.

# matplotlib.pyplot → for plotting.

# LogisticRegression → logistic regression model.

# train_test_split → to split data into training/testing sets.

# Creates array [[0], [1], [2], ..., [9]] → this is our feature.

# .reshape(-1,1) turns it into 2D shape (10 rows, 1 column) as required by scikit-learn.

# y = np.array([0 if i % 2 == 0 else 1 for i in X.flatten()])
#Creates label array:
    #0 for even numbers
    #1 for odd numbers
    #Example: y = [0,1,0,1,0,1,0,1,0,1]
    
# 70% training, 30% testing

# Random state ensures reproducibility.

# This is important for measuring how well the model generalizes.

# LogisticRegression() creates a logistic regression classifier.

# .fit() learns the weight (slope) and intercept (bias) of the sigmoid function that best separates class 0 vs class 1.

# predict() gives the final class (0 or 1).

# predict_proba() gives the probabilities for both classes.

# Example for a single point: [0.8, 0.2] means 80% chance class 0, 20% chance class 1.

# We take many x points from -1 to 10 to plot a smooth curve.

# predict_proba()[:, 1] extracts the probability of class “1” (odd) at each point.

# Result is a sigmoid curve:
    #Low probability for small even numbers
    #High probability for large odd numbers
    #Gradual transition near the decision boundary.
    
# 🟡 What the plot shows:
    #Blue circles (o) → Training samples
    #Red or black crosses (x) → Test samples (unseen during training)
    #Black sigmoid curve → Probability of being odd (class 1)
    #Dashed horizontal line at 0.5 → threshold where class changes

# 👉 The black/red cross mark (marker='x') simply represents the test data points. We use a different shape to visually distinguish between train and test data.
    #Points below the 0.5 line → classified as even (0)
    #Points above → classified as odd (1).