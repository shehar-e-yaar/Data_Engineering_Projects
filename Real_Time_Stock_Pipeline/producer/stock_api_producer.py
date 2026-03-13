import json
import time
from datetime import datetime, timezone
import requests
from kafka import KafkaProducer

API_KEY = "Enter_Your_Api_Here"  # Replace with your Finnhub API key
BASE_URL = "https://finnhub.io/api/v1/quote"
SYMBOLS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]

print("Starting producer...")
print("Connecting to Kafka...")

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    api_version=(0, 10, 1),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=10000
)

print("Connected to Kafka.")

def fetch_quote(symbol: str):
    params = {
        "symbol": symbol,
        "token": API_KEY
    }

    try:
        print(f"Fetching data for {symbol}...")
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()
        print(f"API response for {symbol}: {payload}")

        # Finnhub quote fields:
        # c = current price
        # h = high price of the day
        # l = low price of the day
        # o = open price of the day
        # pc = previous close price
        # t = timestamp
        price = payload.get("c")
        api_timestamp = payload.get("t")

        if price is None or price == 0:
            print(f"No valid price found for {symbol}")
            return None

        # Finnhub quote endpoint may not include volume here,
        # so we keep volume as 0 in version 1.
        event_time = (
            datetime.fromtimestamp(api_timestamp, tz=timezone.utc).isoformat()
            if api_timestamp
            else datetime.now(timezone.utc).isoformat()
        )

        return {
            "symbol": symbol,
            "price": float(price),
            "volume": 0,
            "timestamp": event_time
        }

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

if __name__ == "__main__":
    print("Producer loop started.")
    while True:
        for symbol in SYMBOLS:
            event = fetch_quote(symbol)
            if event:
                producer.send("stock_prices", event)
                producer.flush()
                print(f"Sent: {event}")
        print("Sleeping for 10 seconds...\n")
        time.sleep(10)