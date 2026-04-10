import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Portfolio Overview", page_icon="💼", layout="wide")

st.title("💼 Asset Allocation & Mapping")

# Define base physical & equity holdings
data = {
    "Asset Class": ["Equity", "Equity", "Equity", "Precious Metals", "Precious Metals", "Crypto", "Crypto"],
    "Asset": ["Keppel (BN4.SI)", "OCBC (O39.SI)", "SRT.SI", "Physical Gold", "Physical Silver", "Solana (SOL)", "Flare (FLR)"],
    "Quantity": [1000, 1000, 5000, 73, 91.34, 50, 10000], 
    "Unit": ["Shares", "Shares", "Shares", "Grams", "Troy Oz", "Tokens", "Tokens"]
}

df = pd.DataFrame(data)

st.subheader("Current Tracked Inventory")
st.write("Edit the quantities below to update the allocation visualizer.")

# Editable dataframe to adjust holdings on the fly
edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

st.subheader("Allocation Breakdown (By Asset Class)")
# Simple count visualization based on the table (can be upgraded to live value later)
fig = px.pie(edited_df, names='Asset Class', title='Portfolio Distribution by Class')
st.plotly_chart(fig, use_container_width=True)

st.info("Note: To calculate live portfolio weightings, link the 'Quantity' column to the yfinance real-time price pulls from the Analyst Screener logic.")