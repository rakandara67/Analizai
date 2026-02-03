import streamlit as st
from data import *
from logic import *

st.set_page_config(page_title="Forex Decision Engine", layout="centered")
st.title("Forex Decision Engine (5-Core System)")

pair = st.selectbox("Cütlük:", ["EURUSD", "GBPUSD", "XAUUSD"])

if st.button("Analizi işə sal"):
    htf_df = get_ohlc(pair, "4h")
    ltf_df = get_ohlc(pair, "1h")

    htf = htf_bias(htf_df)
    tech = technical_bias(ltf_df)
    strength = currency_strength(ltf_df)
    retail_pct = get_retail_sentiment(pair)
    retail = retail_bias(retail_pct)
    regime = market_regime(ltf_df)

    st.subheader("Mənbələr:")
    st.write("HTF Bias:", htf)
    st.write("Technical:", tech)
    st.write("Currency Strength:", strength)
    st.write("Retail Sentiment:", retail_pct, "%")
    st.write("Market Regime:", regime)

    if regime == "RANGE":
        st.warning("Range bazarı — trend trade risklidir")

    result = final_decision({
        "htf": htf,
        "technical": tech,
        "strength": strength,
        "retail": retail
    })

    st.success("YEKUN QƏRAR: " + result)
