import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import requests
import json
from datetime import date

st.title('Hello')

ts_price_response = requests.get('https://api.coingecko.com/api/v3/coins/ravencoin/market_chart?vs_currency=usd&days=11430&interval=daily')
ts_price_dict = json.loads(ts_price_response.text)
ts_prices = ts_price_dict["prices"]
ts_market_caps = ts_price_dict["market_caps"]
ts_total_volumes = ts_price_dict["total_volumes"]

ts = [ts_price[0] for ts_price in ts_prices]
ymd_date = [date.fromtimestamp(t/1000) for t in ts]
prices = [ts_price[1] for ts_price in ts_prices]
market_caps = [ts_market_cap[1] for ts_market_cap in ts_market_caps]
total_volumes = [ts_total_volume[1] for ts_total_volume in ts_total_volumes]

combined_data = list(map(list,zip(ts,ymd_date,prices,market_caps,total_volumes)))

df = pd.DataFrame(combined_data, columns=["timestamp", "date","price","market_cap","total_volume"])
df["sma_4y"] = df.price.rolling(1458).mean()
df.index=ymd_date
st.line_chart(df[["price","sma_4y"]])
df