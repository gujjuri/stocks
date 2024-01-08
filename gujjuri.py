import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta
import time

# Function to download data (cached)
@st.cache_data
def download_data(tickers):
    end_date = pd.to_datetime('today')
    start_date = end_date - timedelta(days=360)
    df = pd.DataFrame()
    for ticker in tickers:
        time.sleep(0.2)  # Time lag
        try:
            data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
            df[ticker] = data
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")
            return None
    return df if not df.empty else None

# Function to get data for a specific period
def get_data_for_period(df, days):
    end_date = pd.to_datetime('today')
    start_date = end_date - timedelta(days=days)
    return df.loc[start_date:end_date]

# Function to calculate cumulative relative returns

def calculate_cumulative_returns(df):
    daily_returns = df.pct_change().ffill()  # Forward fill for null values
    cumulative_returns = (1 + daily_returns).cumprod() - 1
    return cumulative_returns



def relativeret_1yr(df):
    rel = df.pct_change()
    cumret= (1+rel).cumprod()-1
    cumret = cumret.fillna(0)
    return cumret

def identify_top_momentum_stocks(best_performers_dict):
    all_stocks = sum(best_performers_dict.values(), [])
    stock_frequency = {}

    for stock in all_stocks:
        stock_frequency[stock] = stock_frequency.get(stock, 0) + 1

    sorted_stocks = sorted(stock_frequency.items(), key=lambda x: x[1], reverse=True)
    top_stocks = [stock for stock, freq in sorted_stocks if freq > 1]
    return top_stocks

def identify_top_weak_stocks(worst_performers_dict):
    all_stocks = sum(worst_performers_dict.values(), [])
    stock_frequency = {}

    for stock in all_stocks:
        stock_frequency[stock] = stock_frequency.get(stock, 0) + 1

    sorted_stocks = sorted(stock_frequency.items(), key=lambda x: x[1], reverse=True)
    weak_stocks = [stock for stock, freq in sorted_stocks if freq > 1]
    return weak_stocks



# Streamlit App Setup
st.title("Streamlit Finance Dashboard")


# Define your list of tickers
tickers = ['^NSEI', 'SUPREMEIND.NS', 'ELECON.NS', 'TASTYBITE.NS', 'ROTO.NS', 'SENCO.NS', 'GREENPLY.NS', 'RADIANTCMS.NS', 
    'OLECTRA.NS', 'EXIDEIND.NS', 'POWERGRID.NS',  'TATAELXSI.NS',  'SULA.NS', 
    'BSE.NS', 'CDSL.NS', 'CAMS.NS', 'FINEORG.NS', 'MANAPPURAM.NS', 'PRINCEPIPE.NS', 'DMART.NS', 'BALAMINES.NS', 
    'RADICO.NS', 'VBL.NS', 'PETRONET.NS', 'KOTAKBANK.NS', 'SYNGENE.NS', 'VOLTAS.NS', 'PAGEIND.NS', 'MGL.NS', 
    'TORNTPHARM.NS', 'BALRAMCHIN.NS', 'MCDOWELL-N.NS', 'IGL.NS', 'DALBHARAT.NS', 'COLPAL.NS', 'NAVINFLUOR.NS', 
    'IBULHSGFIN.NS', 'INDHOTEL.NS', 'INDIAMART.NS', 'BIOCON.NS', 'CROMPTON.NS', 'SRF.NS', 'ZEEL.NS', 'JUBLFOOD.NS', 
    'GUJGASLTD.NS', 'LALPATHLAB.NS', 'PVRINOX.NS', 'MFSL.NS', 'COFORGE.NS', 'DIVISLAB.NS', 'ABBOTINDIA.NS', 
    'AARTIIND.NS', 'DEEPAKNTR.NS', 'LUPIN.NS', 'CONCOR.NS', 'TVSMOTOR.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'MARICO.NS', 
    'BHARTIARTL.NS', 'SUNPHARMA.NS', 'GAIL.NS', 'PIIND.NS', 'CHOLAFIN.NS', 'ABB.NS', 'GNFC.NS', 'ESCORTS.NS', 
    'HDFCBANK.NS', 'CUMMINSIND.NS', 'AUROPHARMA.NS', 'METROPOLIS.NS', 'BOSCHLTD.NS', 'TITAN.NS', 'IPCALAB.NS', 
    'DELTACORP.NS', 'ZYDUSLIFE.NS', 'HDFCLIFE.NS', 'BALKRISIND.NS', 'NESTLEIND.NS', 'HINDUNILVR.NS', 'ATUL.NS',
    'CHAMBLFERT.NS', 'HAL.NS', 'BATAINDIA.NS', 'UBL.NS', 'INDIGO.NS', 'ITC.NS', 'BPCL.NS', 'TATACONSUM.NS', 
    'DRREDDY.NS', 'DABUR.NS', 'ULTRACEMCO.NS', 'SIEMENS.NS', 'ALKEM.NS', 'ICICIPRULI.NS', 'TRENT.NS', 'PIDILITIND.NS', 
    'MCX.NS', 'TATACOMM.NS', 'SBILIFE.NS', 'LAURUSLABS.NS', 'APOLLOHOSP.NS', 'SBICARD.NS', 'ADANIENT.NS', 
    'RELIANCE.NS', 'OBEROIRLTY.NS', 'BAJAJFINSV.NS', 'VEDL.NS', 'OFSS.NS', 'NAUKRI.NS', 'GODREJCP.NS', 'ONGC.NS', 
    'MRF.NS', 'LICHSGFIN.NS', 'GRANULES.NS', 'AUBANK.NS', 'ADANIPORTS.NS', 'ICICIGI.NS', 'CANFINHOME.NS', 
    'ASIANPAINT.NS', 'POLYCAB.NS', 'BAJFINANCE.NS', 'BERGEPAINT.NS', 'CUB.NS', 'MUTHOOTFIN.NS', 'LTTS.NS', 
    'BHARATFORG.NS', 'UPL.NS', 'BAJAJ-AUTO.NS', 'TCS.NS', 'RBLBANK.NS', 'HEROMOTOCO.NS', 'BANKBARODA.NS', 
    'SUNTV.NS', 'GODREJPROP.NS', 'SBIN.NS', 'M&M.NS', 'HAVELLS.NS', 'SHREECEM.NS', 'IRCTC.NS', 'SHRIRAMFIN.NS', 
    'TATAMOTORS.NS', 'PERSISTENT.NS', 'POWERGRID.NS', 'BSOFT.NS', 'IOC.NS', 'LT.NS', 'INDUSTOWER.NS', 'EICHERMOT.NS', 
    'COALINDIA.NS', 'JKCEMENT.NS', 'DLF.NS', 'RAMCOCEM.NS', 'HINDPETRO.NS', 'ASHOKLEY.NS', 'LTIM.NS', 'HDFCAMC.NS', 
    'BANDHANBNK.NS', 'INFY.NS', 'BEL.NS', 'EXIDEIND.NS', 'ABFRL.NS', 'M&MFIN.NS', 'HCLTECH.NS',  
    'INDIACEM.NS', 'TATAPOWER.NS', 'COROMANDEL.NS', 'IDFCFIRSTB.NS', 'HINDZINC.NS', 'MARUTI.NS', 'ICICIBANK.NS', 
    'TECHM.NS', 'ASTRAL.NS', 'IDFC.NS', 'AXISBANK.NS', 'JSWSTEEL.NS', 'FEDERALBNK.NS', 'AMBUJACEM.NS', 'WIPRO.NS', 
    'PEL.NS', 'GLENMARK.NS', 'APOLLOTYRE.NS', 'GRASIM.NS', 'CANBK.NS', 'RECLTD.NS', 'BOSCHLTD.NS', 'HAPPSTMNDS.NS', 
    'CYIENT.NS', 'AFFLE.NS', 'PERSISTENT.NS', 'ZENSARTECH.NS']





# Main App
df = download_data(tickers)

if df is not None:
    best_performers_dict = {}
    worst_performers_dict = {}
    time_frames = [360, 180, 90, 45]

    for days in time_frames:
        df_period = get_data_for_period(df, days)
        cumulative_returns = calculate_cumulative_returns(df_period)
        final_day_performance = cumulative_returns.iloc[-1]
        best_performers = final_day_performance.sort_values().tail(9)
        best_performers_dict[days] = best_performers.index.tolist()
        # Evaluate performance on the last day of each period
       
        worst_performers = final_day_performance.sort_values().head(9)
        worst_performers_dict[days] = worst_performers.index.tolist()
        final_day_performance = cumulative_returns.iloc[-1]
        # Display the best performers
        st.header(f'Best Performers over {days} Days')
        st.write(best_performers)
        st.line_chart(cumulative_returns[best_performers.index])

        # Display the worst performers
        st.header(f'Worst Performers over {days} Days')
        st.write(worst_performers)
        st.line_chart(cumulative_returns[worst_performers.index])
       
    # Identify top momentum stocks
    top_momentum_stocks = identify_top_momentum_stocks(best_performers_dict)
    top_weak_stocks = identify_top_weak_stocks(worst_performers_dict)

    # Input for total funds and calculate investment
    total_funds = st.text_input("Enter total investment funds", "10000")
    invest_button = st.button("Calculate Investment")

    if invest_button and total_funds:
        try:
            total_funds = float(total_funds)
            fund_per_stock = total_funds / len(top_momentum_stocks)

            st.header("Investment per Stock")
            for stock in top_momentum_stocks:
                if stock in df.columns:
                    current_price = df[stock].iloc[-1]  # Last available price
                    quantity = fund_per_stock / current_price
                    st.write(f"{stock}: Invest {fund_per_stock:.2f}, Quantity: {quantity:.2f}")
                else:
                    st.write(f"Data not available for {stock}")

        except ValueError:
            st.error("Please enter a valid number for total funds.")

else:
    st.error("Failed to fetch data. Please check the tickers and try again.")
##############################
    


st.title("Stramlit Finance Dashboard")

tickers1 = ('^NSEI', 'SUPREMEIND.NS', 'ELECON.NS', 'TASTYBITE.NS', 'ROTO.NS', 'SENCO.NS', 'GREENPLY.NS', 'RADIANTCMS.NS', 
    'OLECTRA.NS', 'EXIDEIND.NS', 'POWERGRID.NS', 'MOTHERSUMI.NS', 'TATAELXSI.NS', 'AMARAJABAT.NS', 'SULA.NS', 
    'BSE.NS', 'CDSL.NS', 'CAMS.NS', 'FINEORG.NS', 'MANAPPURAM.NS', 'PRINCEPIPE.NS', 'DMART.NS', 'BALAMINES.NS', 
    'RADICO.NS', 'VBL.NS', 'PETRONET.NS', 'KOTAKBANK.NS', 'SYNGENE.NS', 'VOLTAS.NS', 'PAGEIND.NS', 'MGL.NS', 
    'TORNTPHARM.NS', 'BALRAMCHIN.NS', 'MCDOWELL-N.NS', 'IGL.NS', 'DALBHARAT.NS', 'COLPAL.NS', 'NAVINFLUOR.NS', 
    'IBULHSGFIN.NS', 'INDHOTEL.NS', 'INDIAMART.NS', 'BIOCON.NS', 'CROMPTON.NS', 'SRF.NS', 'ZEEL.NS', 'JUBLFOOD.NS', 
    'GUJGASLTD.NS', 'LALPATHLAB.NS', 'PVRINOX.NS', 'MFSL.NS', 'COFORGE.NS', 'DIVISLAB.NS', 'ABBOTINDIA.NS', 
    'AARTIIND.NS', 'DEEPAKNTR.NS', 'LUPIN.NS', 'CONCOR.NS', 'TVSMOTOR.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'MARICO.NS', 
    'BHARTIARTL.NS', 'SUNPHARMA.NS', 'GAIL.NS', 'PIIND.NS', 'CHOLAFIN.NS', 'ABB.NS', 'GNFC.NS', 'ESCORTS.NS', 
    'HDFCBANK.NS', 'CUMMINSIND.NS', 'AUROPHARMA.NS', 'METROPOLIS.NS', 'BOSCHLTD.NS', 'TITAN.NS', 'IPCALAB.NS', 
    'DELTACORP.NS', 'ZYDUSLIFE.NS', 'HDFCLIFE.NS', 'BALKRISIND.NS', 'NESTLEIND.NS', 'HINDUNILVR.NS', 'ATUL.NS',
    'CHAMBLFERT.NS', 'HAL.NS', 'BATAINDIA.NS', 'UBL.NS', 'INDIGO.NS', 'ITC.NS', 'BPCL.NS', 'TATACONSUM.NS', 
    'DRREDDY.NS', 'DABUR.NS', 'ULTRACEMCO.NS', 'SIEMENS.NS', 'ALKEM.NS', 'ICICIPRULI.NS', 'TRENT.NS', 'PIDILITIND.NS', 
    'MCX.NS', 'TATACOMM.NS', 'SBILIFE.NS', 'LAURUSLABS.NS', 'APOLLOHOSP.NS', 'SBICARD.NS', 'ADANIENT.NS', 
    'RELIANCE.NS', 'OBEROIRLTY.NS', 'BAJAJFINSV.NS', 'VEDL.NS', 'OFSS.NS', 'NAUKRI.NS', 'GODREJCP.NS', 'ONGC.NS', 
    'MRF.NS', 'LICHSGFIN.NS', 'GRANULES.NS', 'AUBANK.NS', 'ADANIPORTS.NS', 'ICICIGI.NS', 'CANFINHOME.NS', 
    'ASIANPAINT.NS', 'POLYCAB.NS', 'BAJFINANCE.NS', 'BERGEPAINT.NS', 'CUB.NS', 'MUTHOOTFIN.NS', 'LTTS.NS', 
    'BHARATFORG.NS', 'UPL.NS', 'BAJAJ-AUTO.NS', 'TCS.NS', 'RBLBANK.NS', 'HEROMOTOCO.NS', 'BANKBARODA.NS', 
    'SUNTV.NS', 'GODREJPROP.NS', 'SBIN.NS', 'M&M.NS', 'HAVELLS.NS', 'SHREECEM.NS', 'IRCTC.NS', 'SHRIRAMFIN.NS', 
    'TATAMOTORS.NS', 'PERSISTENT.NS', 'POWERGRID.NS', 'BSOFT.NS', 'IOC.NS', 'LT.NS', 'INDUSTOWER.NS', 'EICHERMOT.NS', 
    'COALINDIA.NS', 'JKCEMENT.NS', 'DLF.NS', 'RAMCOCEM.NS', 'HINDPETRO.NS', 'ASHOKLEY.NS', 'LTIM.NS', 'HDFCAMC.NS', 
    'BANDHANBNK.NS', 'INFY.NS', 'BEL.NS', 'EXIDEIND.NS', 'ABFRL.NS', 'M&MFIN.NS', 'HCLTECH.NS', 'MOTHERSON.NS', 
    'INDIACEM.NS', 'TATAPOWER.NS', 'COROMANDEL.NS', 'IDFCFIRSTB.NS', 'HINDZINC.NS', 'MARUTI.NS', 'ICICIBANK.NS', 
    'TECHM.NS', 'ASTRAL.NS', 'IDFC.NS', 'AXISBANK.NS', 'JSWSTEEL.NS', 'FEDERALBNK.NS', 'AMBUJACEM.NS', 'WIPRO.NS', 
    'PEL.NS', 'GLENMARK.NS', 'APOLLOTYRE.NS', 'GRASIM.NS', 'CANBK.NS', 'RECLTD.NS', 'BOSCHLTD.NS', 'HAPPSTMNDS.NS', 
    'CYIENT.NS', 'AFFLE.NS', 'PERSISTENT.NS', 'ZENSARTECH.NS')

dropdown = st.multiselect("pick your stock",tickers1)
start = st.date_input("Start",value=pd.to_datetime('2021-01-01'))
end = st.date_input("End",value=pd.to_datetime('today'))

def relativeret_1yr(df):
    rel = df.pct_change()
    cumret= (1+rel).cumprod()-1
    cumret = cumret.fillna(0)
    return cumret


if len(dropdown)>0:
    #df = yf.download(dropdown,start,end)['Adj Close']
    df = relativeret_1yr(yf.download(dropdown,start,end)['Adj Close'])
    st.header('Returns of {}'.format(dropdown))
    st.line_chart(df)


