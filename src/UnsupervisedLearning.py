import numpy as np
from sklearn.cluster import KMeans

# ---- Data ----
X = np.array([[1], [2], [3], [10], [11], [12]])

# ---- KMeans Clustering ----
kmeans = KMeans(n_clusters=2, random_state=0)
kmeans.fit(X)

# ---- Predict Cluster ----
clusters = kmeans.predict(X)

for num, cluster in zip(X.flatten(), clusters):
    print(f"{num} ➝ Cluster {cluster}")
