import yfinance as yf
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def stock_prediction(stock_name: str, days_of_prediction: int) -> list[int]:
    # Get Stock Data from API, example: AAPL
    df = yf.Ticker(stock_name).history(period="1y")
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

    # Combination of both models = predict next value
    # Prediction of the next 30 Values
    last_prices = np.array(df.values[-last_values - 1:]).ravel()  # Calc with last 55 changes/diffs = last 56 values
    predictions = []

    for i in range(days_of_prediction):
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

    print(predictions)
    
    return predictions