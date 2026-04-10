import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Analyst Screener", page_icon="🎯", layout="wide")

st.title("🎯 Bulk Forecast Scanner")
st.write("Aggregating current consensus price targets for monitored equities.")

# Pre-loaded with local SGX and US Tech
default_tickers = "BN4.SI, O39.SI, SRT.SI, NVDA, MSFT, AAPL"
tickers_input = st.text_area("Enter tickers to scan (comma separated):", default_tickers)

if st.button("Run Scan"):
    ticker_list = [t.strip() for t in tickers_input.split(",")]
    results = []
    
    progress_text = "Scanning financial feeds..."
    my_bar = st.progress(0, text=progress_text)
    
    for i, t in enumerate(ticker_list):
        try:
            stock = yf.Ticker(t)
            info = stock.info
            
            curr = info.get('currentPrice', info.get('regularMarketPrice'))
            target = info.get('targetMeanPrice')
            
            upside = None
            if curr and target:
                upside = ((target - curr) / curr) * 100
                
            results.append({
                "Symbol": t,
                "Name": info.get('shortName', t),
                "Currency": info.get('currency', ''),
                "Current Price": curr,
                "Target Price (Mean)": target,
                "Implied Upside (%)": upside,
                "Analyst Recommendation": info.get('recommendationKey', 'N/A').replace('_', ' ').title()
            })
        except Exception as e:
            results.append({"Symbol": t, "Name": "Error pulling data"})
            
        my_bar.progress((i + 1) / len(ticker_list), text=progress_text)
        
    my_bar.empty()
    
    df = pd.DataFrame(results)
    # Format the dataframe for better display
    st.dataframe(
        df.style.format({
            "Current Price": "{:.2f}",
            "Target Price (Mean)": "{:.2f}",
            "Implied Upside (%)": "{:.2f}%"
        }).background_gradient(subset=["Implied Upside (%)"], cmap="Greens"),
        use_container_width=True
    )