import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score

# Get Stock Data from API
df = yf.Ticker("AAPL").history(period="1y")
df['Average'] = (df['High'] + df['Low'] + df['Close'] + df['Open']) / 4
df = df[["Average"]]

# Little optimum for Apple
last_values = 55

# Get data
changes = np.diff(np.array(df.values).ravel())
all_x_and_y = [(changes[i:i + last_values], (changes[i + last_values] > 0).astype(int)) for i in  # TODO: sum better!?!?
               range(changes.shape[0] - last_values)]

changes, target_labels = np.array([x for x, _ in all_x_and_y]), np.array([y for _, y in all_x_and_y])

# Split Data in Training- and Validationsets
X_train, X_test, y_train, y_test = train_test_split(changes, target_labels, test_size=0.2, shuffle=False, stratify=None)

# Create and configure Logistic Regression
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

# Prediction
y_pred = log_reg.predict(X_test)

# Accuracy of the prediction
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Plot Data of the prediction
fig, ax = plt.subplots(nrows=2, ncols=1)
ax[0].plot(np.arange(X_train.shape[0]), y_train)
ax[0].plot(np.arange(X_train.shape[0], X_train.shape[0] + X_test.shape[0]), y_test)
ax[0].plot(np.arange(X_train.shape[0], X_train.shape[0] + X_test.shape[0]), y_pred)
ax[1].plot(np.arange(df.shape[0] - last_values - 1), df.values[last_values + 1:])
plt.legend()
plt.show()

# Prediction of next absolute difference
changes = np.abs(np.diff(np.array(df.values).ravel()))
all_x_and_y = [(changes[i:i + last_values], changes[i + last_values]) for i in
               range(changes.shape[0] - last_values)]  # Labels: next change

changes, target_labels = np.array([x for x, _ in all_x_and_y]), np.array([y for _, y in all_x_and_y])

# Split Data in Training- and Validationsets
X_train_change, X_test_change, y_train_change, y_test_change = train_test_split(changes, target_labels, test_size=0.2, shuffle=False, stratify=None)

# Create and Configure Random Forest Regressor
rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X_train_change, y_train_change)

# Prediction of the change
predicted_changes = rf_reg.predict(X_test_change)

# Plot of actual and predicted changes
fig, ax = plt.subplots(nrows=2, ncols=1)
ax[0].plot(np.arange(X_train_change.shape[0]), y_train_change, color="royalblue")
ax[0].plot(np.arange(X_train_change.shape[0], X_train_change.shape[0] + X_test_change.shape[0]), y_test_change, color="orange")
ax[0].plot(np.arange(X_train_change.shape[0], X_train_change.shape[0] + X_test_change.shape[0]), predicted_changes, color="green")
ax[1].plot(np.arange(df.shape[0] - last_values - 1), df.values[last_values + 1:])
plt.legend()
plt.show()

# Combination of both models = predict next value
# Prediction of the next 30 Values
num_predictions = 30
last_prices = np.array(df.values[-last_values - 1:]).ravel()  # Calc with last 55 changes/diffs = last 56 values
predictions = []

for i in range(num_predictions):
    changes = np.array([np.diff(last_prices).ravel()])

    # Prediction of direction and magnitude
    direction = log_reg.predict(changes)[0]
    magnitude = rf_reg.predict(np.abs(changes))[0]

    if direction == 1:
        next_price = last_prices[-1] + magnitude
    else:
        next_price = last_prices[-1] - magnitude

    predictions.append(next_price)
    last_prices = np.append(last_prices[1:], next_price)

# Plot of historic Data and Prediction
plt.figure(figsize=(10, 6))
plt.plot(np.arange(df.shape[0]), df.values, label='Historic Data')
plt.plot(np.arange(df.shape[0], df.shape[0] + num_predictions), predictions, label='Predicted Values',
         color='red')
plt.legend()
plt.show()