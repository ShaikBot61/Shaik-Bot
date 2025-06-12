import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_signal():
    message = """
📡 *SHAiK BOT SIGNAL 🔥*

🔴 *Signal Type:* SELL  
📊 *Pair:* BTCUSD  
🕒 *Timeframe:* H1

────────────────────

📌 *WHY This Trade?* [Complete Logic]

1. 💥 *SMC*: Break of structure + retest into Bearish OB  
2. 🕳️ *ICT*: FVG filled, liquidity taken above high → bearish setup  
3. 💢 *RSI = 75* → Overbought  
4. 📉 *MACD*: Bearish crossover  
5. 🧱 *EMA*: EMA 21 < EMA 50 → Bearish trend forming  
6. ⚠️ *Chart Pattern*: Rising wedge breakdown confirmed  
7. 📈 *Candle*: Bearish pinbar rejecting OB  
8. 🧠 *Psychology*: Retail traders trapped long → Market reversing  
9. 📉 *News*: Sentiment negative due to ETF delay rumors  

────────────────────

🎯 *Trade Setup*:

📍 *Entry:* 67280.00  
🛑 *SL:* 67600.00  
🥅 *TP:* 65800.00  
📏 *Risk:* 1.5% | 📐 R:R = 1:3  
🔢 *Lot:* 0.01

────────────────────

💡 *Summary:*  
> "Liquidity grab completed, SMC and ICT align perfectly. RSI and MACD agree, news sentiment negative. Smart entry for profit-taking."

📬 *Sent at:* 17:40 GMT  
🔗 *Powered by Shaik Bot 🧠*
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, data=data)
    print(response.json())

send_signal()