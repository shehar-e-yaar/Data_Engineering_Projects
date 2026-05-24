import requests
import json
import psycopg2
from datetime import datetime
DB_HOST = "localhost"
DB_NAME = "mydb"
DB_USER = "crypto_user"
DB_PASS = "mypassword"
DB_PORT = "5433"

def savetopostgres(coinname,price):
   conn=None
   try:
      conn=psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
      )
      cursor=conn.cursor()
      create_table_query ="""CREATE TABLE IF NOT EXISTS crypto_prices (
            id SERIAL PRIMARY KEY,
            coin_name VARCHAR(50),
            price_usd NUMERIC(15, 2),
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
      cursor.execute(create_table_query)
      insert_query = """
      INSERT INTO crypto_prices (coin_name, price_usd) 
      VALUES (%s, %s);
      """
      cursor.execute(insert_query, (coinname, price))
      conn.commit()
      print(f"[{datetime.now()}] Successfully saved {coinname} price (${price}) to Postgres!")
   except Exception as e:
      print(f"Error saving to Postgres: {e}")

   finally:
      if conn is not None:
         cursor.close()
         conn.close()

def fetch_live_price():
      url="https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin&x_cg_demo_api_key=CG-G2tGTRQeXwZnpi7uxRq4LQVq"
      response = requests.get(url)
      data = response.json() 
    
   
      if 'bitcoin' in data:
        
        btc_data = data.get('bitcoin')
        
       
        if 'usd' in btc_data:
            price = btc_data.get('usd')
            print(f"Success! Price is: ${price}")
            savetopostgres("bitcoin", price)
        
        else:
            print("Error: 'usd' column JSON mein nahi mila!")
      else:
       print("Error: 'bitcoin' column JSON mein nahi mila!")
fetch_live_price()