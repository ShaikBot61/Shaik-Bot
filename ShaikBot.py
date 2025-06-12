import os
import requests
import pandas as pd
import schedule
import time
from dotenv import load_dotenv
import telegram
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=BOT_TOKEN)

def fetch_price_data(symbol):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100'
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])

    df['close'] = df['close'].astype(float)
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    return df

def analyze_market(symbol, pair_name):
    df = fetch_price_data(symbol)

    rsi = RSIIndicator(close=df['close'], window=14).rsi()
    macd = MACD(close=df['close']).macd_diff()
    ema_21 = EMAIndicator(close=df['close'], window=21).ema_indicator()
    ema_50 = EMAIndicator(close=df['close'], window=50).ema_indicator()

    latest_rsi = rsi.iloc[-1]
    latest_macd = macd.iloc[-1]
    latest_ema21 = ema_21.iloc[-1]
    latest_ema50 = ema_50.iloc[-1]
    latest_price = df['close'].iloc[-1]

    signal_type = None
    reasons = []

    if latest_rsi > 70:
        signal_type = "SELL"
        reasons.append("RSI > 70 (Overbought)")
    elif latest_rsi < 30:
        signal_type = "BUY"
        reasons.append("RSI < 30 (Oversold)")

    if latest_macd > 0:
        reasons.append("MACD: Bullish crossover")
        if signal_type is None:
            signal_type = "BUY"
    elif latest_macd < 0:
        reasons.append("MACD: Bearish crossover")
        if signal_type is None:
            signal_type = "SELL"

    if latest_ema21 > latest_ema50:
        reasons.append("EMA Trend: Bullish")
    else:
        reasons.append("EMA Trend: Bearish")

    if signal_type:
        message = f"""
📡 SHAiK BOT SIGNAL 🔥

🟢 Signal Type: {signal_type}
📊 Pair: {pair_name}
🕒 Timeframe: 1H

────────────────────

📌 WHY This Trade?

""" + '\n'.join([f"✅ {r}" for r in reasons]) + f"""

🎯 Entry: {latest_price:.2f}
🛑 SL: Auto Calculated
🥅 TP: Auto Calculated
📏 Risk: 1.5% | 📐 R:R = 1:2
🔢 Lot: 0.01

────────────────────

💡 Summary:
> Based on RSI, MACD, and EMA, this is a strategic {signal_type} opportunity.

🔗 Powered by Shaik Bot 🧠
"""

        bot.send_message(chat_id=CHAT_ID, text=message)

# Run for both symbols
def run_bot():
    analyze_market("BTCUSDT", "BTCUSD")
    analyze_market("XAUUSDT", "XAUUSD")

# Schedule every 1 hour
schedule.every(1).hours.do(run_bot)

print("Shaik Bot Started... 🚀")
while True:
    schedule.run_pending()
    time.sleep(1)
