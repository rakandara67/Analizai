import requests
import pandas as pd
import streamlit as st

# =========================================
# TwelveData API üçün key təhlükəsiz çıxarış
# =========================================
def get_api_key():
    try:
        return st.secrets["38d2782acb57431f84806652c8828407"]
    except KeyError:
        st.error("TWELVEDATA_API_KEY Streamlit Secrets-də yoxdur. App dayandırıldı!")
        st.stop()

# =========================================
# OHLC Data çəkmək
# =========================================
def get_ohlc(symbol, interval, bars=300):
    apikey = get_api_key()
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": bars,
        "apikey": apikey
    }

    r = requests.get(url, params=params).json()

    # error handling
    if "values" not in r:
        st.error(f"Data alınmadı: {r.get('message', 'unknown error')}")
        st.stop()

    df = pd.DataFrame(r["values"])
    df = df.astype(float)
    return df.iloc[::-1]  # ən yeni data sonda

# =========================================
# Retail Sentiment (Myfxbook) – müvəqqəti sadə
# =========================================
def get_retail_sentiment(symbol):
    # burada Myfxbook login mövcuddursa əlavə et
    # yoxsa default 50%
    st.info("Retail sentiment funksiyası hazırda test üçün default 50% qaytarır")
    return 50.0
