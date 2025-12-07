import pandas as pd
data=pd.read_csv('city_data.csv')
data.head()

data["name"]=data["name"].str.strip().str.capitalize()
data["city"]=data["city"].str.strip().str.capitalize()
data["sales"]=data["sales"].astype(int)
data["bonus"]=data["sales"]*0.10

data.to_csv('cleaned_city_data.csv', index=False)
print("Data cleaning complete. Cleaned data saved to 'cleaned_city_data.csv'.")