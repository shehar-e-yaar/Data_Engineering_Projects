CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    price NUMERIC(10,2),
    volume BIGINT,
    event_time TIMESTAMP
);