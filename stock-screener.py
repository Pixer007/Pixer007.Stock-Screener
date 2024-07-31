import pandas as pd
import requests
import streamlit as st
import yfinance as yf
import plotly.express as px
import datetime
import numpy as np
from stocknews import StockNews
from pyChatGPT import ChatGPT

st.markdown("""
    <audio autoplay loop>
        <source src="Scam-1992(PaglaSongs).mp3" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """, unsafe_allow_html=True)
base_url = 'https://financialmodelingprep.com/api'
apikey = 'Wy9h7tdS2JIBadpIs8LaUPA4l5vf3ZoL'


st.header("Paisa Stock Screener")
symbol = st.sidebar.text_input('Ticker: ', value='MSFT')
financial_chart = st.sidebar.selectbox('Visual Charts', options=(
    'Charts','Visual-Charts'
))
if(financial_chart == 'Charts'):
    default_start_date = datetime.date(2024, 2,13)
    start_date = st.sidebar.date_input('Start Date',value=default_start_date)
    end_date = st.sidebar.date_input('End Date')
    financial_chart = yf.download(symbol,start=start_date,end=end_date)
    fig = px.line(financial_chart,x=financial_chart.index,y=financial_chart['Adj Close'],title=symbol)
    st.plotly_chart(fig)
pricing_data,news,price_check = st.tabs(['Pricing Data','News10','Price Checker'])
with pricing_data:
    st.header('Price Movements')
    fin_data = financial_chart
    fin_data['% Change'] = financial_chart['Adj Close'] / financial_chart['Adj Close'].shift(1) - 1
    fin_data.dropna(inplace=True)
    st.write(fin_data)
    annual_return = fin_data['% Change'].mean()*252*100
    st.write('Annual Return = ',annual_return,'%')
    stdev = np.std(fin_data['% Change'])*np.sqrt(252)
    st.write('Standard Deviation = ',stdev*100,'%')
    risk_adj = annual_return/(stdev*100)
    st.write('Risk Adjacency = ',risk_adj)
    if(risk_adj > 1.5):
        st.write('Is Company Considerable = Yes')
    else:
        st.write('Is Company Considerable = No')
with news:
    st.header(f'Top 10 News of {symbol}')
    sn = StockNews(symbol, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment = {news_sentiment}')

with price_check:
    st.header('Price Checker For Reliance, Infosys, TCS')


  
st.header('Financial Matrix')
financial_data = st.sidebar.selectbox('Financial Data Type', options=(
'income-statement', 'balance-sheet-statement', 'cash-flow-statement', 'income-statement-growth',
'balance-sheet-statement-growth', 'cash-flow-statement-growth', 'key-metrics-ttm', 'enterprise-values', 'rating',
'ratios', 'ratios-ttm', 'quote', 'Historical Price smaller intervals'))
if (financial_data == 'Historical Price smaller intervals'):
    interval = st.sidebar.selectbox('Interval', options=('1min', '5min', '15min', '30min', '1hour', '4hour'))
    financial_data = 'historical-chart/' + interval
transpose = st.sidebar.selectbox('Transpose', options=('Yes', 'No'))

url = f'{base_url}/v3/{financial_data}/{symbol}?period=annual&apikey={apikey}'
response = requests.get(url)
data = response.json()

if transpose == 'Yes':
    df = pd.DataFrame(data).T
else:
    df = pd.DataFrame(data)

st.write(df)
