import ta
import numpy as np

# 1️⃣ HTF Market Structure
def htf_bias(df):
    high = df["high"]
    low = df["low"]

    if high.iloc[-1] > high.iloc[-20] and low.iloc[-1] > low.iloc[-20]:
        return "LONG", 0.8
    if high.iloc[-1] < high.iloc[-20] and low.iloc[-1] < low.iloc[-20]:
        return "SHORT", 0.8
    return "NEUTRAL", 0.4

# 2️⃣ Technical Indicators (LTF)
def technical_bias(df):
    ema50 = ta.trend.ema_indicator(df["close"], 50)
    ema200 = ta.trend.ema_indicator(df["close"], 200)
    rsi = ta.momentum.rsi(df["close"], 14)

    if ema50.iloc[-1] > ema200.iloc[-1] and rsi.iloc[-1] < 70:
        return "LONG", 0.7
    if ema50.iloc[-1] < ema200.iloc[-1] and rsi.iloc[-1] > 30:
        return "SHORT", 0.7
    return "NEUTRAL", 0.4

# 3️⃣ Currency Strength (sadə, amma effektiv)
def currency_strength(df):
    returns = df["close"].pct_change().dropna()
    score = returns.tail(20).sum()

    if score > 0.01:
        return "LONG", 0.6
    if score < -0.01:
        return "SHORT", 0.6
    return "NEUTRAL", 0.4

# 4️⃣ Retail Sentiment (Contrarian)
def retail_bias(long_pct):
    if long_pct > 65:
        return "SHORT", 0.7
    if long_pct < 35:
        return "LONG", 0.7
    return "NEUTRAL", 0.4

# 5️⃣ Market Regime
def market_regime(df):
    atr = ta.volatility.average_true_range(
        df["high"], df["low"], df["close"], 14
    )
    if atr.iloc[-1] > atr.mean():
        return "TREND"
    return "RANGE"

def score(sig):
    return {"LONG": 1, "SHORT": -1, "NEUTRAL": 0}[sig]

def final_decision(signals):
    weights = {
        "htf": 0.30,
        "technical": 0.25,
        "strength": 0.20,
        "retail": 0.15
    }

    total = (
        score(signals["htf"][0]) * weights["htf"] * signals["htf"][1] +
        score(signals["technical"][0]) * weights["technical"] * signals["technical"][1] +
        score(signals["strength"][0]) * weights["strength"] * signals["strength"][1] +
        score(signals["retail"][0]) * weights["retail"] * signals["retail"][1]
    )

    if total > 0.25:
        return f"%{int(abs(total)*100)} ehtimalla LONG"
    if total < -0.25:
        return f"%{int(abs(total)*100)} ehtimalla SHORT"
    return "NEUTRAL"
