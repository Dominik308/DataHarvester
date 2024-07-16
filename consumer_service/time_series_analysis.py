import matplotlib.pyplot as plt
import yfinance as yf

from statsmodels.tsa.arima.model import ARIMA


def arima_forecast(last_values: list[float]) -> float:
    """Time series analysis - Define the ARIMA model and do prediction/forecast of next value"""

    # Fit the model
    # Some valid and useful combinations: (0, 1, 0), (10, 2, 0), (20, 2, 0) => not more with this little data set!!!
    model = ARIMA(last_values, order=(0, 1, 0))  # (p, d, q) = (<last values>, <count of differentiations>, <last errors>)
    model_fit = model.fit()  # Resulting model

    # Make next prediction
    predictions = model_fit.forecast()
    prediction = predictions[0]

    return prediction


if __name__ == "__main__":
    df = yf.Ticker("AAPL").history(period="1y")
    df['Average'] = (df['High'] + df['Low'] + df['Close'] + df['Open']) / 4
    df = df[["Average"]]

    # Split data into train data (80%) and test data (20%)
    size = int(df.shape[0] * 0.8)
    train_data, test_data = df.values[0:size], df.values[size:df.shape[0]]
    current_history = list(train_data)
    model_predictions = []

    # Walk-forward validation
    for test_datum in test_data:
        # Make next prediction
        model_prediction = arima_forecast(current_history)
        model_predictions.append(model_prediction)

        # Add test datum to history for predicting next value of test data
        current_history.append(test_datum)

    # Plot results/compare predictions with real data (= test data)
    plt.figure(figsize=(12, 6), dpi=100)
    plt.plot(df[size:].index, test_data, label='Real')
    plt.plot(df[size:].index, model_predictions, color='red', label='Predicted')
    plt.title('ARIMA Predictions vs Actual Values')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()
