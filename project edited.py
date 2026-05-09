import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Stock Market Analysis System") #Create Title
symbol = st.text_input("Enter Stock Symbol") # Create Input Box


if symbol:
    stock = yf.Ticker(symbol) # Fetch Stock Data

    period = st.selectbox(
    "Select Time Period",
    ["7d", "1mo", "3mo", "6mo", "1y"]
    ) # Create Dropdown for Time Period Selection
    data = stock.history(period=period) # Get Historical Data for the selected period


    if data.empty: # Handle Errors
        st.error("Invalid stock symbol")
    else:
        st.write(data) # Show Stock Information
        # -----------------------------------------------------------
        current_price = data["Close"].iloc[-1]
        open_price = data["Open"].iloc[-1]
        high_price = data["High"].max()
        low_price = data["Low"].min()
        avg_volume = int(data["Volume"].mean())

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Current Price", f"{current_price:.2f}")
        col2.metric("Open", f"{open_price:.2f}")
        col3.metric("High", f"{high_price:.2f}")
        col4.metric("Low", f"{low_price:.2f}")
        col5.metric("Avg Volume", f"{avg_volume:,}") # it means how many stock shares were bought/sold. 
#       # Suppose volumes are:
        # Day	     |   Volume
        # Monday	 |   1 Million
        # Tuesday	 |   2 Million
        # Wednesday	 |   3 Million

        # Average volume:
        # (1M + 2M + 3M) / 3 = 2Million shares traded on average.
        # ---------------------------------------------------------
        
        st.write("Current Price:", data["Close"].iloc[-1])

        # Create Line Chart for Stock Price Trend
        fig = px.line(data, y="Close", title="Stock Price Trend")
        st.plotly_chart(fig)

        # Average Closing Price # george's part
        average_price = data["Close"].mean()
        st.write("Average Closing Price:", round(average_price, 2))

        # -----------------------------
        # Hassan Part
        # -----------------------------

        # Daily Price Change
        data["Daily Price Change"] = data["Close"].diff()

        # Percentage Change
        data["Percentage Change"] = data["Close"].pct_change() * 100

        # Display Daily Price Change
        st.subheader("Daily Price Change")
        st.write(data["Daily Price Change"])

        # Display Percentage Change
        st.subheader("Percentage Change (%)")
        st.write(data["Percentage Change"])

        # ------------------------------        
        # George's Part
        # -----------------------------
        
        # 7-Day Moving Average
        data["Moving Average"] = data["Close"].rolling(5).mean()
        fig = px.line(data, y=["Close", "Moving Average"], )
        st.plotly_chart(fig)

        #------------------------------
        #John part
        #------------------------------
        
        #figure 1
        st.subheader("Volume Chart")

        fig1, ax1 = plt.subplots(figsize=(12, 6))
        ax1.bar(data.index, data["Volume"])
        ax1.set_title("Trading Volume")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Volume")

        st.pyplot(fig1)
        st.divider()
        
        #figure 2
        st.subheader("High vs Low Chart")

        fig2, ax2 = plt.subplots(figsize=(12, 6))

        ax2.plot(data.index, data["High"], label="High Price")
        ax2.plot(data.index, data["Low"], label="Low Price")

        ax2.set_title("High vs Low Prices")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Price")
        ax2.legend()

        st.pyplot(fig2)
        st.divider() 
        
        #figure 3
        st.subheader("Moving Average Chart")

        fig3, ax3 = plt.subplots(figsize=(12, 6))

        ax3.plot(data.index, data["Close"], label="Closing Price")
        ax3.plot(data.index, data["Moving Average"], label="7-Day Moving Average")

        ax3.set_title("Moving Average Analysis")
        ax3.set_xlabel("Date")
        ax3.set_ylabel("Price")
        ax3.legend()

        st.pyplot(fig3)
        st.divider()

       
