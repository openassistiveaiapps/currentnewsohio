import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

data = {'Size': [1000, 1500, 1800, 2400, 3000],
        'Price': [200000, 250000, 280000, 350000, 400000]}
df = pd.DataFrame(data)
X = df[['Size']]
y = df['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

print("Coef:", model.coef_)
print("Intercept:", model.intercept_)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("y_test:", y_test.values)
print("y_pred:", y_pred)
print("MSE:", mse, "RMSE:", rmse, "R2:", r2)

# Plot training points and best-fit line
plt.scatter(X_train, y_train, color='blue', label='Train')
plt.scatter(X_test, y_test, color='green', label='Test')
xs = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
plt.plot(xs, model.predict(xs), color='red', label='Fit')
plt.legend()
plt.xlabel('Size (sqft)')
plt.ylabel('Price ($)')
plt.title('Linear Regression Demo')
plt.show()



# train_test_split: utility to split data into training and testing sets.

# LinearRegression: ordinary least squares linear model from scikit-learn.

# mean_squared_error: evaluation metric (MSE) for regression.

# pandas as pd: DataFrame handling (tabular data).

# We create a small dictionary with two columns: Size (feature) and Price (label).

# pd.DataFrame(data) converts the dictionary to a tabular DataFrame:

#   Size   Price
# 0 1000  200000
# 1 1500  250000
# 2 1800  280000
# 3 2400  350000
# 4 3000  400000

# X must be 2-D for scikit-learn (n_samples × n_features). Using df[['Size']] returns a DataFrame with shape (5,1).

# y is a 1-D Series (shape (5,)) representing the target values.

# Important: passing df['Size'] (a Series) to fit would work too for a single feature (scikit-learn handles it), 
# but keeping X as a 2-D array/dataframe is clearer and consistent for multiple features.

# test_size=0.2 → 20% of data for testing, 80% for training. With 5 rows, test_size=0.2 yields 1 test sample and 4 training samples.

# random_state=42 seeds the random number generator so the split is reproducible (same split every run).

# Why split? So we can measure performance on unseen data and detect overfitting.

# LinearRegression() by default fits an intercept (bias term).

# .fit(X_train, y_train) computes the best-fit line (ordinary least squares) that minimizes the sum of squared residuals on the training data.

# After fitting you can inspect:
# model.coef_ → slope(s), array shape (n_features,)
# model.intercept_ → intercept scalar

# y_pred is an array of predicted prices for the test Size values.
# Because we only had 1 test sample (due to small dataset), y_pred will be length 1.

# MSE = average of squared differences between actual and predicted values:
    # Lower MSE → better fit.
    # With tiny test set (1 sample) MSE is not a stable metric — use larger test sets or cross-validation for real evaluation