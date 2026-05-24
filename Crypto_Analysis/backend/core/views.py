from django.http import JsonResponse
from django.shortcuts import render
import psycopg2
import joblib
import os
import pandas as pd
import requests
def get_prediction(request):
    try:
        
        conn = psycopg2.connect(
            host="db", database="mydb", user="crypto_user", password="mypassword", port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT price_usd FROM crypto_prices ORDER BY fetched_at DESC LIMIT 1;")
        live_price = cursor.fetchone()[0]
        cursor.close()
        conn.close()

      
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=8&interval=daily"
        data = requests.get(url).json()
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        
        
        price_1_day_ago = df['price'].iloc[-2]
        price_2_days_ago = df['price'].iloc[-3]
        moving_avg_7 = df['price'].tail(7).mean()

        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'crypto_model.pkl')
        model = joblib.load(model_path)
        
        predicted_price = model.predict([[price_1_day_ago, price_2_days_ago, moving_avg_7]])[0]

        
        return render(request, 'index.html', {
            'live_price': live_price,
            'predicted_price': predicted_price
        })
        

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})