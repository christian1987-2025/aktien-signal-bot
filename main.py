import yfinance as yf
import requests
import time
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message}
    )

def check_rsi_signal(ticker):
    try:
        data = yf.download(ticker, period="14d", interval="1h")
        close = data["Close"].dropna()
        if len(close) < 14:
            return
        delta = close.diff()
        gain = delta.clip(lower=0).mean()
        loss = -delta.clip(upper=0).mean()
        rs = gain / loss if loss != 0 else 100
        rsi = 100 - (100 / (1 + rs))
        if rsi < 30:
            send_telegram_message(f"📉 Kaufsignal: {ticker} (RSI: {rsi:.2f})")
        elif rsi > 70:
            send_telegram_message(f"📈 Verkaufssignal: {ticker} (RSI: {rsi:.2f})")
    except Exception as e:
        print(f"Fehler bei {ticker}: {e}")

TICKERS = ["NVDA", "AAPL", "TSLA", "AMD", "MSFT", "AMZN"]

send_telegram_message("✅ Bot wurde erfolgreich gestartet.")

while True:
    for sym in TICKERS:
        check_rsi_signal(sym)
    time.sleep(1800)
