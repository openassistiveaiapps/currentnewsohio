from sklearn.linear_model import LogisticRegression
import numpy as np
import matplotlib.pyplot as plt

X = np.array([[i] for i in range(1, 21)])
y = np.array([1 if i % 2 == 0 else 0 for i in range(1, 21)]) # Even=1, Odd=0

model = LogisticRegression()
model.fit(X, y)

X_test = np.array([[21], [22], [23], [24]])
y_pred = model.predict(X_test)

plt.scatter(X, y, c=y, cmap='coolwarm', s=100)
plt.scatter(X_test, y_pred, c='black', marker='X', s=200)
plt.yticks([0, 1], ['Odd', 'Even'])
plt.xlabel('Number')
plt.title('Even/Odd Classification')
plt.show()
