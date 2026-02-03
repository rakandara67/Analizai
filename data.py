import requests
import pandas as pd
import streamlit as st

def get_ohlc(symbol, interval, bars=300):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": bars,
        "apikey": st.secrets["TWELVEDATA_API_KEY"]
    }
    r = requests.get(url, params=params).json()
    df = pd.DataFrame(r["values"])
    df = df.astype(float)
    return df.iloc[::-1]

def get_retail_sentiment(symbol):
    login = requests.get(
        "https://www.myfxbook.com/api/login.json",
        params={
            "email": st.secrets["MYFXBOOK_EMAIL"],
            "password": st.secrets["MYFXBOOK_PASSWORD"]
        }
    ).json()

    session = login["session"]
    data = requests.get(
        "https://www.myfxbook.com/api/get-community-outlook.json",
        params={"session": session}
    ).json()

    for s in data["symbols"]:
        if s["name"] == symbol:
            return float(s["longPercentage"])

    return 50.0
