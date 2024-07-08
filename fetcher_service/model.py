import yfinance as yf
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


def create_dataset(dataset, time_step: int) -> tuple[np.array:, np.array]:
    """Create datasets: "time_step many data" to predict next data (e.g. 60er packets)"""
    data_x, data_y = [], []

    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        data_x.append(a)
        data_y.append(dataset[i + time_step, 0])

    return np.array(data_x), np.array(data_y)


# Parameter
time_step = 120

# 1. Get data
ticker = 'AAPL'
data = yf.download(ticker, start='2019-07-01', end='2024-07-01')
data = data[['Close']]

# 2. Prepare data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Create data sets
X, y = create_dataset(scaled_data, time_step)

# Split data into train data and test data
train_size = int(len(X) * 0.8)
test_size = len(X) - train_size
train_X, test_X = X[0:train_size], X[train_size:len(X)]
train_y, test_y = y[0:train_size], y[train_size:len(y)]

# Reshape data for LSTM [samples, time steps, features]
train_X = train_X.reshape(train_X.shape[0], train_X.shape[1], 1)
test_X = test_X.reshape(test_X.shape[0], test_X.shape[1], 1)

# 3. Create model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# Compile model with square loss and adam
model.compile(optimizer='adam', loss='mean_squared_error')

# Train model with train data
model.fit(train_X, train_y, batch_size=1, epochs=10)

# Make predictions for last time
train_predict = model.predict(train_X)
test_predict = model.predict(test_X)

# Scale data back (back from intial preparing data)
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

# Plot predictions
plt.figure(figsize=(14, 5))
plt.plot(data.index, data["Close"])
plt.plot(data.index[-test_predict.shape[0]:], test_predict, label='Testing Data Prediction')
plt.legend()
plt.show()

# Make predictions for next 30 days
count_of_next_days = 120
last_days = scaled_data[-time_step:]
next_days_prediction = []

for _ in range(count_of_next_days):
    last_days = last_days.reshape(1, time_step, 1)
    predicted_price = model.predict(last_days)
    next_days_prediction.append(predicted_price[0, 0])
    last_days = np.append(last_days[0, 1:], predicted_price, axis=0)

next_days_prediction = scaler.inverse_transform(np.array(next_days_prediction).reshape(-1, 1))

# Plot predictions
plt.figure(figsize=(14, 5))
plt.plot(range(len(data)), data['Close'], label='Original Data')
plt.plot(range(len(data), len(data) + count_of_next_days), next_days_prediction,
         label=f'Next {count_of_next_days} Days Prediction', color='red')
plt.legend()
plt.show()
