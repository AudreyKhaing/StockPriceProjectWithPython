
#Ploting Tesla and GameStop Stock Prices

#Installing Packages
!pip install yfinance==0.1.67
!mamba install bs4==4.10.0 -y
!pip install nbformat==4.2.0

#Importing Libraries
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Graph Function
#Parameters to input are a dataframe with stock data (dataframe must contain Date and Close columns), a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


#Creating stock ticker for Telsa
tesla = yf.Ticker("TSLA")


#Saving the stock information (history) in datafarme
tesla_data = tesla.history(period="max")

#Resetting the index and seeing the top 5 records
tesla_data.reset_index(inplace=True)
tesla_data.head()

#Scraping the URL and assigning the result to text
tesla_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data  = requests.get(tesla_url).text

#Passing the HTML data into beautiful soup object
tesla_soup = BeautifulSoup(html_data, "html.parser")

#Creating a data frame and looping through beautifulsoup object to pass the contents to data frame
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tesla_soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True) 

#Removing $ signs from revenue column
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")

#Removing empty strings and null values from revenue column
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

#Passing the revenue from String to Int and seeing the last 5 records 
tesla_revenue['Revenue'] = pd.to_numeric(tesla_revenue['Revenue'])
tesla_revenue.tail()








#Creating stock ticker for GameStop
gamestock = yf.Ticker("GME")

#Saving the stock information (history) in datafarme
gamestock_data = gamestock.history(period="max")

#Resetting the index and seeing the top 5 records
gamestock_data.reset_index(inplace=True)
gamestock_data.head()

#Scraping the URL and assigning the result to text
gamestock_url = " https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
gshtml_data  = requests.get(gamestock_url).text

#Passing the HTML data into beautiful soup object
gamestock_soup = BeautifulSoup(gshtml_data, "html.parser")

#Creating a data frame and looping through beautifulsoup object to pass the contents to data frame
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in gamestock_soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)

#Removing $ signs from revenue column
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")

#Removing empty strings and null values from revenue column
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

#Passing the revenue from String to Int and seeing the last 5 records 
gme_revenue['Revenue'] = pd.to_numeric(gme_revenue['Revenue'])
gme_revenue.tail()

#Calling the make_graph method to graph historical data and revenue data 
make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(gamestock_data, gme_revenue, 'GameStop')
