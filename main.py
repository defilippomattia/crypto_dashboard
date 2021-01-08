import streamlit as st
import pandas as pd
import numpy as np
from cryptocmd import CmcScraper
import requests
import json
from urllib.request import urlopen

#st.set_page_config(layout="wide")
#streamlit run main.py
# cd .\ENV-crypto\Scripts\
#30c7f2e66699271d0d030ad54336135ef882bc51 

coins = ["BTC","ETH","DOT"]

github_repositories = {
    "BTC": "https://api.github.com/repos/bitcoin/bitcoin/stats/participation",
    "DOT": "https://api.github.com/repos/paritytech/polkadot/stats/participation",
    "ETH": "https://api.github.com/repos/ethereum/go-ethereum/stats/participation"   
}

def get_historical_data(crypto,first_day,last_day):
    scraper = CmcScraper(crypto,first_day,last_day)
    historical_data_df = scraper.get_dataframe().set_index("Date")
    return historical_data_df

def get_coin_selected():
    coin = st.sidebar.selectbox("Select coin",coins)
    return coin

def draw_closing_price():
    global historical_data_df
    st.subheader("Closing price")
    st.line_chart(historical_data_df["Close"])

def draw_volatility():
    global historical_data_df
    st.subheader("Volatility")
    st.line_chart(historical_data_df["Close"].pct_change())

def draw_custom():
    global historical_data_df
    st.subheader("Custom graph")
    default_columns = ["Volume", "Market Cap"]
    st_ms = st.multiselect("Columns", historical_data_df.columns.tolist(), default=default_columns)
    st.line_chart(historical_data_df[st_ms])

def draw_github_commits(coin):
    url = github_repositories[coin]
    response = urlopen(url)
    string_response = response.read().decode('utf-8')
    dictionary_response = json.loads(string_response)
    commits_by_week = list(dictionary_response["all"])
    commits_by_week_df = pd.DataFrame(commits_by_week,columns=["commits"])
    st.subheader("Github commits (last 52 weeks)")
    st.line_chart(commits_by_week_df["commits"])


coin = get_coin_selected()
st.title(coin + ' dashboard')

historical_data_df = get_historical_data(coin, "1-1-2020", "5-1-2021")

draw_closing_price()
draw_volatility()
draw_custom()
draw_github_commits(coin)


