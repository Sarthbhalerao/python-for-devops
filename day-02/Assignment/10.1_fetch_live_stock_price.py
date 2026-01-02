import requests
import json
from datetime import date
import sys
api_key = "XHO2NC2K600K48HN" 
# complete API URL : https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo

api_url = "https://www.alphavantage.co/" # Base URL
query_function = "TIME_SERIES_DAILY"

def validate_date_range(start_date, end_date):
    # Allowed date range
    min_date = "2025-08-05"
    max_date = str(date.today())  # Today's date
    # Validate Start Date
    if start_date < min_date or start_date > max_date:
        print(f"\n Invalid Start Date: {start_date}")
        print(f"Please enter a date between {min_date} and {max_date}")
        return False
    # Validate End Date
    if end_date < min_date or end_date > max_date:
        print(f"\nInvalid End Date: {end_date}")
        print(f" Please enter a date between {min_date} and {max_date}")
        return False
    # Logical Check
    if end_date < start_date:
        print("\nEnd date cannot be earlier than start date!")
        return False
    return True

def fetch_stock_price(symbol, start_date, end_date):
    url = f"{api_url}query?function={query_function}&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Save raw data
        with open(f'raw_{symbol}_stock_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4) 
        print(f"\nSuccessfully fetched data for: {symbol}") 

        time_series = data.get("Time Series (Daily)", {})
        open_close_prices = {} # To store filtered data
        print(f"\nStock Data for {symbol} between {start_date} and {end_date}:\n")
        for date_key, price_info in time_series.items():
            if date_key < start_date or date_key > end_date:
                continue  # Ignore dates outside range
            open_price = price_info["1. open"]
            close_price = price_info["4. close"]
            open_close_prices[date_key] = {"open": open_price, "close": close_price}
            print(f"Date: {date_key} | Open: {open_price} | Close: {close_price}")
        # Save filtered data to a new JSON file
        with open(f'{symbol}_open_close_prices.json', 'w') as json_file:
            json.dump(open_close_prices, json_file, indent=4)

        print("\nFiltered data saved successfully!")
    else:
        print(f"API request failed. Status Code: {response.status_code}")
# added code to accept command line arguments
if len(sys.argv) == 4:
    symbol = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    if validate_date_range(start_date, end_date):
        fetch_stock_price(symbol, start_date, end_date)
    else:
        print("Date validation failed. Please check the input dates.")
else:
    symbol = input("Enter the stock symbol (e.g., IBM, AAPL, GOGL, AMZN): ")   
    # Input date range from user (ONLY runs in else)
    while True:
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        if validate_date_range(start_date, end_date):
            break
        else:
            print("Date validation failed. Please check the input dates.")

    fetch_stock_price(symbol, start_date, end_date)
   
         