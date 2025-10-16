import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans

# ================================
# 🧠 1. RULE-BASED LEARNING
# ================================
numbers = np.arange(1, 21)
labels = ["Even" if n % 2 == 0 else "Odd" for n in numbers]

# Plot
plt.figure(figsize=(6, 2))
colors = ['orange' if l == "Even" else 'blue' for l in labels]
plt.scatter(numbers, [0]*len(numbers), c=colors, s=100)
plt.yticks([])
plt.title("🧠 Rule-Based: Even/Odd Classification")
plt.xlabel("Number")
plt.show()

# Print predictions
for n, l in zip(numbers, labels):
    print(f"{n} ➝ {l}")


# ================================
# 🤖 2. SUPERVISED LEARNING (Logistic Regression)
# ================================
# Training data (even/odd)
X_train = numbers.reshape(-1, 1)
y_train = np.array([1 if n % 2 == 0 else 0 for n in numbers])

model = LogisticRegression()
model.fit(X_train, y_train)

# Test
X_test = np.array([[21], [22], [23], [24]])
preds = model.predict(X_test)

# Plot
plt.figure(figsize=(6, 2))
plt.scatter(X_train, y_train, c=y_train, cmap='coolwarm', s=100)
plt.scatter(X_test, preds, c=preds, marker='X', s=200, edgecolors='k')
plt.yticks([0, 1], ['Odd', 'Even'])
plt.title("🤖 Supervised: Logistic Regression")
plt.xlabel("Number")
plt.show()

# Print predictions
for n, p in zip(X_test.flatten(), preds):
    label = "Even" if p == 1 else "Odd"
    print(f"{n} ➝ {label}")


# ================================
# 🌀 3. UNSUPERVISED LEARNING (K-Means)
# ================================
X_unsup = np.array([[1], [2], [3], [10], [11], [12]])
kmeans = KMeans(n_clusters=2, random_state=0)
kmeans.fit(X_unsup)
clusters = kmeans.predict(X_unsup)

# Plot
plt.figure(figsize=(6, 2))
plt.scatter(X_unsup, [0]*len(X_unsup), c=clusters, cmap='viridis', s=200)
plt.scatter(kmeans.cluster_centers_, [0, 0], c='red', s=300, marker='X', label='Centroids')
plt.yticks([])
plt.title("🌀 Unsupervised: K-Means Clustering")
plt.xlabel("Number")
plt.legend()
plt.show()

# Print cluster assignment
for num, cluster in zip(X_unsup.flatten(), clusters):
    print(f"{num} ➝ Cluster {cluster}")
