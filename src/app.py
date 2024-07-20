import os
import dash
import requests
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.svm import SVR
import plotly.express as px
from dotenv import load_dotenv
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from sklearn.linear_model import LinearRegression
from dash.dependencies import Input, Output, State
from sklearn.model_selection import train_test_split

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

app = dash.Dash(__name__)
app.suppress_callback_exceptions = True
app.title = "Stock Sense"
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="shortcut icon" type="image/png" href="/assets/logo.ico">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
server = app.server
app.layout = html.Div(
    [
    html.Div([
              html.Div([
        html.P("Welcome to the Stock Visualization & Forecast App!", className="project-heading"),
        html.Div([
                html.Img(src="/assets/bears-removebg-preview.png", className="title-card"),
            ], className="image-container"),
            html.P("Heye, Please enter legitimate stock code to get the details.")
        ], className="content-container"),
              html.Div([
                       
                        html.P("Input Stock Code :", className="stock"),
                        dcc.Input(
                            id='stock-input-id',
                            className="stock-input",
                            type='text',
                            value='',
                            placeholder='Example - TSLA, MSFT, AAPL',
                        ),
                        html.Div([
                            html.Button(
                                html.Span("SUBMIT", className="inner-span", id='submit-button-id',),
                                className="submit-button"
                            )
                        ], className="flex items-center justify-center content-center text-center w-screen h-screen bg-gray-900"),

                        
                        dcc.ConfirmDialog(
                            id='submit-error-popup',
                            message=''
                        ),
                    ], className="stock-div"
              ),
              html.Div([
                html.P('Pick a Date :', className="pick-date"),
                dcc.DatePickerRange(
                    id='date-picker-range-id',
                    className="date-picker-range",
                    start_date=None,
                    end_date=None,
                    display_format='YYYY-MM-DD',
                ),
                html.Button('STOCK PRICE',  id='stock-price-button-id', className='stock-button stock-price-button cursor-pointer flex items-center bg-lime-950 hover:bg-lime-900 active:border active:border-lime-400 rounded-md duration-100 p-2', n_clicks=0),
                dcc.ConfirmDialog(
                            id='stock-price-error-popup',
                            message=''
                        ),
                html.Button('INDICATOR', id='indicator-button-id', className='indicator-button cursor-pointer flex items-center bg-lime-950 hover:bg-lime-900 active:border active:border-lime-400 rounded-md duration-100 p-2', n_clicks=0),
                 dcc.ConfirmDialog(
                            id='indicator-error-popup',
                            message=''
                ),
              ], className="date-picker-div"
              ),

              html.Div([
                       dcc.Input(
                            id='forecast-input-id',
                            className="forecast-input",
                            type='text',
                            value='',
                            placeholder='Enter the no. of days to get forecast',
                       ),
                        html.Button('FORECAST', id='forecast-button-id', n_clicks=0, className="button forecast-button cursor-pointer flex items-center bg-lime-950 hover:bg-lime-900 active:border active:border-lime-400 rounded-md duration-100 p-2"),
                        dcc.ConfirmDialog(
                            id='forecast-error-popup',
                            message=''
                        ),
                    ], className="forecast-div"
              ),
    ], className="division1", id="division-1-id",
    ),

    html.Div(
        [
            html.Div([
                    html.P("", id='name-id',  className="company-name"),
                    html.Br(),
                    html.Img(src='', id='logo-id', className="company-logo"),
                ],
                className="header"
            ),
            html.Br(),
            html.Div([
             ], id="description", className="description_ticker"),
            html.Br(),
            html.Div([
                dcc.Graph(id='stock-graph-id', style={'visibility': 'hidden'})
            ], className='graph-container'),
            html.Br(),
            html.Div([
                dcc.Graph(id="indicator-graph-id", style={'visibility': 'hidden'})
            ], className='graph-container'),
            html.Br(),
            html.Div([
                dcc.Graph(id="forecast-graph-id", style={'visibility': 'hidden'})
            ], className='graph-container'),
            html.Br(),
            html.Br(),
        ],
        className="division2", id="division-2-id",
    )
  ], 
  className="container content"
)

@app.callback(
    [
        Output("name-id", "children"),
        Output("logo-id", "src"),
        Output("description", "children"),
    ],
    Input("submit-button-id", "n_clicks"),
    State("stock-input-id", "value"),
    prevent_initial_call=True
)
    
def update_data(submit_button, stock_input):
    if submit_button is None:
        return dash.no_update
 
    if not stock_input:
        print("No stock selected")
        return dash.no_update
    
    ticker = yf.Ticker(stock_input)
    inf = ticker.info

    df = pd.DataFrame().from_dict(inf, orient="index").T
    print(df.to_dict())
    print(df["longBusinessSummary"])

    # Assuming df is your DataFrame
    shortName = df["shortName"].to_list()
    longName = df["longName"].to_list()

    print(shortName)
    print(longName)
    name_string = longName[0] 
    words = name_string.split()
    print(words)  
    # Output: ['Microsoft', 'Corporation']
    # cleaned_names = [re.sub(r'[^a-zA-Z]', '', word) for word in words]
    # Access each word individually
    first_word = words[0]
    second_word = words[1]

    print(first_word)  # Output: 'Microsoft'
    print(second_word)  # Output: 'Corporation'
    company_logo = fetch_logo(longName[0])
    
    # company_desc= df["longBusinessSummary"]
    try:
        company_desc = df["longBusinessSummary"]
    except KeyError:
        company_desc = f'Description for {stock_input} is not available. \nPlease check the stock symbol or try again later.'
    except Exception as e:
        company_desc = f'An error occurred while retrieving the description for {stock_input}'
    return longName[0], company_logo,  company_desc
    
    
def fetch_logo(company_name) :
    """Fetches the company logo using Google Knowledge Search API"""
    print(f"Received Company name : {company_name}")
    url = f'https://kgsearch.googleapis.com/v1/entities:search?query={company_name}&key={GOOGLE_API_KEY}&limit=1&indent=True'
    response = requests.get(url).json()

    if 'itemListElement' in response and len(response['itemListElement']) > 0:
        if 'image' in response['itemListElement'][0]['result']:
            logo_url = response['itemListElement'][0]['result']['image']['contentUrl']
            print('Logo found')
            return logo_url
        else:
            print('Logo not found')
            return 'https://iili.io/dF0GdyG.png'
    else:
        print('Logo not found')
        return 'https://iili.io/dF0GdyG.png'
    
def fetch_desc(company_name):
    """Fetches the company logo using POLYGON.IO API"""
    company = str(company_name)
    print(company)
    url = f"https://api.polygon.io/v3/reference/tickers/{company}?apiKey={GOOGLE_API_KEY}"
    data = requests.get(url=url)
    data = data.json()
    # print(data)
    if data.get('status') == "OK":
        print("Status OKAY")
        if 'results' in data:
            if 'description' in data['results']:
                desc = data['results'].get('description')
                return str(desc)
            else:
                print('Description not found in results')
        else:
            print('Results not found in response')
    else:
        print('Status not OKAY')

    return 'Description Not Available'


@app.callback(
    Output('stock-graph-id', 'figure'),
    Output('stock-graph-id', 'style'),
    [
        Input('stock-price-button-id', 'n_clicks'),
    ],
    [
        State("stock-input-id", "value"),
        State('date-picker-range-id', 'start_date'),
        State('date-picker-range-id', 'end_date'),
    ],
    prevent_initial_call=True
)

def update_graph(stock_price_button, stock_symbol, start_date, end_date):
    if stock_price_button is None:
        return dash.no_update
    
    if not stock_symbol:
        print("No stock selected")
        return dash.no_update
    
    if not start_date or not end_date:
        print("Stock selected, but dates not selected")
        return dash.no_update
        # return {}, {'visibility' : 'hidden'}, True, 'Dates are not selected'
    
    df = yf.download(tickers=stock_symbol, start=start_date, end=end_date)
    if df.empty:
        print("No data available for this stock symbol.") 
        return dash.no_update

    df.reset_index(inplace=True)
    fig = get_stock_price_fig(df, stock_symbol)
    return fig, {'visibility': 'visible', 'width' : '80%', 'margin': '0 auto'}

def get_stock_price_fig(dataFrame, stock_symbol):
    # Line Charts
    fig = px.line(dataFrame,
                  x='Date',
                  y=['Open', 'Close'],
                  title=f"{stock_symbol} - Closing and Opening Price vs Date")

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='#1e1e1e',
        font=dict(color='white'),
        xaxis=dict(showgrid=True, gridcolor='white'),
        yaxis=dict(showgrid=True, gridcolor='white')
    )

    return fig

@app.callback (
    [
        Output("indicator-graph-id", "figure"),
        Output("indicator-graph-id", "style"),
    ],
     
    [
        Input("indicator-button-id", "n_clicks")
    ],
    [
        State("stock-input-id", "value"),
        State("date-picker-range-id", "start_date"),
        State("date-picker-range-id", "end_date"),
    ],
    prevent_initial_call=True
)

def update_ema_graph( indicator_button, stock_symbol , start_date, end_date):
    if indicator_button is None:
        return dash.no_update
    
    if not stock_symbol:
        print("No stock selected")
        return dash.no_update
    
    if not start_date or not end_date:
        print("Stock selected, but dates not selected")
        return dash.no_update
    
    df = yf.download(tickers=stock_symbol, start=start_date, end=end_date)
    if df.empty:
        print("No EMA (Exponential Moving Average) available for this stock symbol.")
        return dash.no_update
    
    df.reset_index(inplace=True)
    fig = get_more(df, stock_symbol)
    return fig, {'visibility': 'visible', 'width' : '80%', 'margin': '0 auto'}
    
def get_more(df, stock_symbol):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                     x='Date',
                     y='EWA_20',
                     title=f"{stock_symbol} - Exponential Moving Average (20) vs Date")
    
    # To show the EMA as a line plot
    fig.update_traces(mode='lines')  
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='#1e1e1e',
        font=dict(color='white'),
        xaxis=dict(showgrid=True, gridcolor='white'),
        yaxis=dict(showgrid=True, gridcolor='white')
    )
    return fig

@app.callback (
    [
        Output("forecast-graph-id", "figure"),
        Output("forecast-graph-id", "style"),
    ],
    [
        Input("forecast-button-id", "n_clicks")
    ],
    [
        State("stock-input-id", "value"),
        State("forecast-input-id", "value"),
        State("date-picker-range-id", "start_date"),
        State("date-picker-range-id", "end_date"),
    ],
    prevent_initial_call=True
)

def forecast_graph(forecast_button, stock_symbol, forecast_days, start_date, end_date):
    if forecast_button is None:
        return dash.no_update
    
    START_DATE = pd.Timestamp(end_date) - pd.DateOffset(days=90)
    try :
        df = yf.download(tickers=stock_symbol, start=START_DATE, end=end_date)
    except ValueError:
        return dash.no_update
    
    df = df[['Adj Close']]

    df['Prediction'] = df[['Adj Close']].shift(-int(forecast_days))

    X = np.array(df.drop(['Prediction'], axis=1))[:-int(forecast_days)]

    Y = np.array(df['Prediction'])[:-int(forecast_days)]

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_rbf.fit(x_train, y_train)

    linear_r = LinearRegression()
    linear_r.fit(x_train, y_train)

    x_forecast = np.array(df.drop(['Prediction'], axis=1))[-int(forecast_days):]

    svr_predicted = svr_rbf.predict(x_forecast)
    lr_predicted = linear_r.predict(x_forecast)

    forecast_dates = pd.date_range(start=pd.to_datetime(end_date) + pd.Timedelta(days=1), periods=int(forecast_days))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=forecast_dates, y=svr_predicted, mode='lines', name='SVR Forecast'))
    fig.add_trace(go.Scatter(x=forecast_dates, y=lr_predicted, mode='lines', name='Linear Regression Forecast'))

    fig.update_layout(title=f'{stock_symbol} Stock Price Forecast - {forecast_days} Days',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      template='plotly_dark')

    print("Forecast Figure Received")

    return fig, {'visibility': 'visible', 'width' : '80%', 'margin': '0 auto'}

if __name__ == '__main__':
  app.run(debug=False)