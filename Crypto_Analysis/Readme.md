---
# 🚀 Crypto-Analysis: End-to-End Data & ML Pipeline

A robust, containerized Data Engineering and Machine Learning pipeline that ingests real-time cryptocurrency data, processes it, and serves future price predictions through a Django-powered web dashboard.

This project demonstrates a **"Data-as-a-Product"** mindset, bridging the gap between raw API data extraction, relational storage, and predictive AI modeling.

### 🏗️ Architecture & Workflow

1. **Data Ingestion:** Extracts historical and live Bitcoin market data via the CoinGecko API.
2. **Storage:** securely stores historical data and daily snapshots into a robust PostgreSQL database.
3. **Machine Learning (MLOps):** Utilizes a Scikit-Learn `RandomForestRegressor` to perform feature engineering (Lag Features, Moving Averages) and trains a predictive model, serialized via `joblib`.
4. **Serving / UI:** A Django backend accesses the database, loads the trained `.pkl` model, and serves the predictions visually through an HTML dashboard.
5. **Infrastructure:** Fully containerized using Docker & Docker Compose for seamless, reproducible environments.

### 🛠️ Tech Stack

* **Language:** Python 3.10
* **Data Engineering:** PostgreSQL, Pandas, Requests
* **Machine Learning:** Scikit-Learn, Joblib
* **Backend & Web:** Django, HTML/CSS
* **DevOps:** Docker, Docker Compose

---

### 🚀 Getting Started

#### Prerequisites

Make sure you have [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose installed on your machine.

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Crypto_Analysis.git
cd Crypto_Analysis

```



#### 2. Spin Up the Infrastructure

Build and start the PostgreSQL database and Django web container:

```bash
docker-compose up -d --build

```

#### 3. Initialize Data (First Run Only)

Run the data ingestion script to create the necessary tables and populate the database with the latest price:

```bash
python data_fetcher/fetch_price.py

```

### 4. Train a fresh Machine Learning model:

```bash
python data_fetcher/train_model.py

```

---

### 💻 Usage

Once the containers are running and data is fetched, open your web browser and navigate to:

👉 **`http://localhost:8000/api/predict/`**

You will see a clean web dashboard displaying the live Bitcoin price fetched from the database and the AI-predicted price for tomorrow.

---

### 🧠 Feature Engineering Details

The predictive model does not just look at raw prices. It utilizes calculated context to make informed predictions:

* `price_1_day_ago`: Captures immediate past momentum.
* `price_2_days_ago`: Helps the model understand short-term trajectory.
* `moving_avg_7`: A 7-day rolling average to smooth out daily market noise and identify broader trends.

---
