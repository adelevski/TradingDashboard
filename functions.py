import streamlit as st
import plotly.graph_objects as go
import yfinance as yf


@st.cache(allow_output_mutation=True)
def make_price_chart(name, period, interval):
    history = yf.download(name, period=period, interval=interval)
    fig = go.Figure(
        layout=dict(
            title=f"{name} Price",
            xaxis_title='Time Period',
            yaxis_title='Price ($)',
        )
    )
    fig.add_trace(go.Scatter({"x": history.index, "y": history['Adj Close'], "name": "Price"}))
    return fig


@st.cache
def make_vol_chart(ticker, date):
    calls, puts = ticker.option_chain(date)
    fig = go.Figure(
        layout=dict(
            title=f"{ticker.ticker} vol smile",
            xaxis_title='Strike Price',
            yaxis_title='Implied Volatility',
        )
    )
    fig.add_trace(go.Scatter({"x": calls['strike'], "y": calls['impliedVolatility'], "name": "Calls"}))
    fig.add_trace(go.Scatter({"x": puts['strike'], "y": puts['impliedVolatility'], "name": "Puts"}))
    return fig