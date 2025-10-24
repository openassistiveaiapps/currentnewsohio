import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Customer data [Age, Spending Score]
customers = np.array([
    [18, 90], [19, 88], [20, 85], [23, 80], [25, 77],
    [30, 60], [35, 65], [40, 55], [45, 52], [50, 50],
    [55, 40], [60, 42], [65, 39], [70, 35], [75, 30]
])

# Run K-Means
kmeans = KMeans(n_clusters=3, random_state=0)
labels = kmeans.fit_predict(customers)

# Sort cluster centers by spending score (second column)
sorted_clusters = np.argsort(kmeans.cluster_centers_[:, 1])

# Assign meaning automatically
group_names = {}
group_names[sorted_clusters[2]] = "👦 Young High Spenders"
group_names[sorted_clusters[1]] = "🧑 Middle-Age Moderate Spenders"
group_names[sorted_clusters[0]] = "🧓 Older Low Spenders"

# Print labeled results
for i, label in enumerate(labels):
    print(f"Customer {i+1}: Age={customers[i,0]}, Spending={customers[i,1]} ➝ {group_names[label]}")

# Plot clusters
plt.figure(figsize=(7,5))
plt.scatter(customers[:, 0], customers[:, 1], c=labels, cmap='viridis', s=120)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            c='red', s=200, marker='X', label='Cluster Centers')
plt.title("🛍️ Customer Segmentation (K-Means)")
plt.xlabel("Age")
plt.ylabel("Spending Score")
plt.legend()
plt.show()
