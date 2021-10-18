import streamlit as st
import yfinance as yf
from functions import make_price_chart, make_vol_chart



st.set_page_config(layout="wide")

st.title('TradeDash')

tickers = get_tickers()

col, buff1, buff2 = st.columns([1, 3, 3])
inp = col.text_input("Ticker")


if inp != 'None':
    ticker = yf.Ticker(inp)
    d1 = ticker.history('1d')
    if len(d1) > 0:
        buff1.write("Company")
        buff1.subheader(ticker.info['shortName'])
        change = round(((d1['Close'][0] - d1['Open'][0]) / d1['Open'][0]) * 100, 2)
        buff2.write()
        buff2.metric(label="Today", value=round(d1['Close'][0], 2), delta=f"{change} %")

        col1, col2 = st.columns([4, 4])
        time_frame = col1.selectbox('Price history period', ['1d-5m', '5d-30m','1mo-1d','6mo-1d', 'ytd-1d', '1y-1wk'])
        period, interval = time_frame.split('-')
        price_fig = make_price_chart(ticker.ticker, period, interval)
        col1.plotly_chart(price_fig)

        available_dates = ticker.options
        if available_dates:
            date = col2.selectbox('Options expiration', available_dates)
            vol_fig = make_vol_chart(ticker, date)
            col2.plotly_chart(vol_fig)

        else:
            col2.write("Option chain is not available")
    else:
        st.write("Invalid ticker")
    