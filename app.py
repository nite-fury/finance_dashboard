import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Fin-Intel Dashboard", page_icon="📈", layout="wide")

# ==========================================
# SIDEBAR: Quick Ticker Investigation
# ==========================================
st.sidebar.header("🔍 Quick Ticker Lookup")
ticker_input = st.sidebar.text_input("Enter Ticker (e.g., BN4.SI, SOL-USD):", "BN4.SI")

if ticker_input:
    try:
        stock = yf.Ticker(ticker_input)
        info = stock.info
        
        st.sidebar.subheader(info.get('shortName', ticker_input))
        current_price = info.get('currentPrice', info.get('regularMarketPrice'))
        currency = info.get('currency', '')
        
        if current_price:
            st.sidebar.metric("Current Price", f"{currency} {current_price:.2f}")
        else:
            st.sidebar.metric("Current Price", "Data N/A")
        
        # Analyst Targets
        target_price = info.get('targetMeanPrice')
        if target_price and current_price:
            upside = ((target_price - current_price) / current_price) * 100
            st.sidebar.metric("Analyst Target (Mean)", f"{currency} {target_price:.2f}")
            st.sidebar.metric("Implied Upside", f"{upside:.2f}%")
            
        st.sidebar.divider()
        st.sidebar.write("**Key Stats:**")
        st.sidebar.write(f"52W High: {info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.sidebar.write(f"52W Low: {info.get('fiftyTwoWeekLow', 'N/A')}")
        st.sidebar.write(f"Dividend Yield: {info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "Dividend Yield: N/A")
             
    except Exception as e:
        st.sidebar.error("Could not retrieve data. Check the ticker format.")

# ==========================================
# MAIN PAGE: Macro Overview
# ==========================================
st.title("📈 Macro Market Overview")
st.write("Welcome to the Fin-Intel Hub. Use the sidebar for immediate asset reconnaissance, or navigate the pages for bulk scanning and portfolio mapping.")

st.subheader("Global Market Snapshot")
col1, col2, col3, col4 = st.columns(4)

def get_quick_price(ticker_str):
    try:
        return yf.Ticker(ticker_str).info.get('currentPrice', yf.Ticker(ticker_str).info.get('regularMarketPrice'))
    except:
        return None

with col1:
    st.metric("S&P 500 (SPY)", f"${get_quick_price('SPY') or 'N/A'}")
with col2:
    st.metric("STI (^STI)", f"S${get_quick_price('^STI') or 'N/A'}")
with col3:
    st.metric("Gold (GC=F)", f"${get_quick_price('GC=F') or 'N/A'}")
with col4:
    st.metric("Bitcoin (BTC-USD)", f"${get_quick_price('BTC-USD') or 'N/A'}")