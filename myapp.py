import streamlit as st import plotly.graph_objs as go from binance.client import Client import pandas as pd

Setup Binance client

client = Client()

Streamlit App Config

st.set_page_config(page_title="Divesh Market Zone", layout="centered") st.title("📈 Divesh Market Zone") st.markdown("Live BTC Chart + Signal + Image Upload + Auto Support/Resistance")

📤 Upload Image Section

st.header("📤 Upload Chart Image") uploaded_file = st.file_uploader("Upload your technical setup image", type=["jpg", "png", "jpeg"]) if uploaded_file is not None: st.image(uploaded_file, caption="Uploaded Chart", use_container_width=True)

📊 Get Historical BTC Data

@st.cache_data def get_data(): klines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, limit=100) df = pd.DataFrame(klines, columns=[ 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore' ]) df['high'] = df['high'].astype(float) df['low'] = df['low'].astype(float) return df

data = get_data()

🔍 Auto Support/Resistance

auto_support = data['low'].min() auto_resistance = data['high'].max()

📊 Signal Generator Section

st.header("📊 Signal Generator") current_price = float(client.get_symbol_ticker(symbol="BTCUSDT")['price']) st.metric("Live BTC Price", f"${current_price:,.2f}")

st.write(f"🟢 Auto Support Level: {auto_support:.2f}") st.write(f"🔴 Auto Resistance Level: {auto_resistance:.2f}")

wave1_high = st.number_input("Wave 1 High", value=auto_resistance * 0.98) trend = st.selectbox("Market Trend", ["Uptrend", "Downtrend"])

SL/TP input

sl = st.number_input("Stop Loss (SL)", value=auto_support) tp = st.number_input("Take Profit (TP)", value=auto_resistance)

Signal Logic

signal = "" if trend == "Uptrend" and current_price > wave1_high: signal = "🚀 BUY Signal (Wave 3 Breakout)" elif trend == "Downtrend" and current_price < wave1_high: signal = "📉 SELL Signal (Wave 3 Breakout)" elif trend == "Uptrend" and current_price > auto_resistance: signal = "🔼 BUY Signal (Resistance Break)" elif trend == "Downtrend" and current_price < auto_support: signal = "🔽 SELL Signal (Support Break)" else: signal = "📵 NO TRADING ZONE"

if st.button("Generate Signal"): st.subheader("📡 Signal Output:") st.success(f"{signal}\n🎯 SL: {sl} | 🏁 TP: {tp}")

📉 BTC Chart with Support/Resistance

st.header("📈 Last 100-Hour BTC/USDT Chart") fig = go.Figure() fig.add_trace(go.Scatter(y=data['high'], mode='lines', name='High')) fig.add_trace(go.Scatter(y=data['low'], mode='lines', name='Low')) fig.add_hline(y=auto_support, line=dict(color='blue', dash='dot'), name="Support") fig.add_hline(y=auto_resistance, line=dict(color='red', dash

