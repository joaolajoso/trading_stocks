import yfinance as yf
import streamlit as st
import pandas as pd
from pandas.tseries.offsets import DateOffset

tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0].Symbol.to_list()
#display(tickers)

@st.cache_data
def getData():
  df = yf.download(tickers, start='2019-01-01')
  df = df['Close']
  return df

df = getData()

st.title('Index component per formance of the S&P500')

n = st.number_input('Please provide the performance horizon in months', min_value=1, max_value=36)

def get_ret(df, n):
  previous_prices = df[:df.index[-1]- DateOffset(months=n)].tail(1).squeeze()
  recent_prices = df.loc[df.index[-1]]
  ret_df = recent_prices/previous_prices -1
  return previous_prices.name, ret_df

date, ret_df = get_ret(df, n)
winners, losers = ret_df.nlargest(10), ret_df.nsmallest(10)
winners.name, losers.name = 'winners', 'losers'

st.table(winners)
st.table(losers)


winnerpick = st.selectbox('Pick a winner to visualize: ', winners.index)
st.line_chart(df[winnerpick][date:])

loserpick = st.selectbox('Pick a losers to visualize: ', losers.index)
st.line_chart(df[loserpick][date:])
