# STOCK VISUALIZATION & FORECAST APP
![ZtzMb2ZPbld4kR7jazctr3m3p5E](https://github.com/user-attachments/assets/58f49fb4-1fd8-40af-b3c9-792dde5eaf34)

A web application that visualizes real-time stock data, predicts future stock prices using machine learning models, and provides detailed insights into stock trends. Built with Python and Dash, the app fetches stock data using an API, applies machine learning models for forecasting, and visualizes the results with interactive charts.

## Features

- **Real-Time Stock Data**: Fetch and display real-time stock data from a reliable API source.
- **Stock Price Visualization**: Interactive charts showing stock price trends using Plotly.
- **Stock Price Forecasting**: Predict future stock prices using machine learning models (Support Vector Regression and Linear Regression).
- **User-friendly Interface**: Intuitive and interactive web interface built with Dash.
- **Historical Data Analysis**: View and analyze historical stock data to understand long-term trends.

## Tech Stack

- **Python**: Main programming language used.
- **Dash**: Web framework for building the front-end of the application.
- **Plotly**: Library used for creating interactive graphs and visualizations.
- **Machine Learning Models**:
  - **Support Vector Regression (SVR)**
  - **Linear Regression**
- **API**: [API Name] for fetching real-time stock data (you can replace this with the specific API you're using).
- **Pandas & NumPy**: For data manipulation and processing.
- **scikit-learn**: Used for implementing the machine learning models.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/stock-visualization-forecast-app.git
    cd stock-visualization-forecast-app
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file for your API key:
    ```
    STOCK_API_KEY=your_api_key_here
    ```

4. Run the application:
    ```bash
    python app.py
    ```

5. Open your browser and go to `http://127.0.0.1:8050/` to view the app.

## Usage

1. **Select a Stock**: Input the stock ticker symbol in the search box.
2. **View Stock Data**: See real-time and historical stock data visualized in graphs.
3. **Predict Stock Prices**: The app will use machine learning models to predict future prices based on past data.
4. **Interactive Graphs**: Hover over the charts to view detailed stock information.


## Demonstration : <pre>**[Link to the Demonstration Video](https://youtu.be/NzPVfPM83cU)** </pre>

## Screenshots
![2024-07-21 01_16_13-Greenshot](https://github.com/user-attachments/assets/ae931611-6b53-42bd-9834-4fe218621b0a)
![2024-07-21 01_19_14-Greenshot](https://github.com/user-attachments/assets/6af21764-b84d-43e4-876a-09b7a5fcfa0b)
![2024-07-21 01_23_56-Greenshot](https://github.com/user-attachments/assets/e38f9186-db6a-49ae-9887-5ff69b918efa)

![2024-07-21 01_26_51-Greenshot](https://github.com/user-attachments/assets/2b367260-6ee7-4b63-b5f2-2b24662a2730)



## Future Enhancements

- Add more machine learning models for better predictions.
- Implement additional financial indicators.
- Improve UI with more customization options.
- Add support for multiple stock markets (e.g., NASDAQ, NYSE).

## Contributing

Feel free to contribute to this project. Fork the repository, make your changes, and submit a pull request!


