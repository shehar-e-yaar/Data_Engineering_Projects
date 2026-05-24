import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
import joblib


def fetch_historical_data(days=365):
    """Fetch Bitcoin historical data"""
    
    print(f"Fetching {days} days of historical data...")
    
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={days}&interval=daily"
    
    response = requests.get(url)
    data = response.json()

    prices = data.get('prices', [])

    df = pd.DataFrame(prices, columns=['timestamp', 'price'])

    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df


def prepare_data_for_ml(df):

    print("Preparing data and creating features...")

    # Lag Features
    df['price_1_day_ago'] = df['price'].shift(1)
    df['price_2_days_ago'] = df['price'].shift(2)
    df['price_3_days_ago'] = df['price'].shift(3)

    # Moving averages
    df['7_day_moving_avg'] = df['price'].rolling(window=7).mean()
    df['14_day_moving_avg'] = df['price'].rolling(window=14).mean()

    # Volatility feature
    df['7_day_std'] = df['price'].rolling(window=7).std()

    # Remove NaN values
    df = df.dropna()

    # Features
    X = df[
        [
            'price_1_day_ago',
            'price_2_days_ago',
            'price_3_days_ago',
            '7_day_moving_avg',
            '14_day_moving_avg',
            '7_day_std'
        ]
    ]

    # Target
    y = df['price']

    return X, y


def train_and_save_model(X, y):

    print("Training XGBoost Model...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )

    # XGBoost Model
    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)

    # Error
    error = mean_absolute_error(y_test, predictions)

    print(f"Model trained successfully!")
    print(f"Average Prediction Error: ${error:.2f}")

    # Save model
    joblib.dump(model, 'crypto_model.pkl')

    print("Model saved as 'crypto_model.pkl'")


if __name__ == "__main__":

    df = fetch_historical_data(days=365)

    X, y = prepare_data_for_ml(df)

    train_and_save_model(X, y)