from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

X = np.array([[500], [750], [1000], [1250], [1500], [1750], [2000]])
y = np.array([100000, 150000, 200000, 250000, 300000, 350000, 400000])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

plt.scatter(X_train, y_train, color='blue')
plt.scatter(X_test, y_test, color='green')
plt.plot(X, model.predict(X), color='red')
plt.title('House Price Prediction')
plt.xlabel('Size (sqft)')
plt.ylabel('Price ($)')
plt.show()
