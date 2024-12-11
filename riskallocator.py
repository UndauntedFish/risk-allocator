import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def load_settings():
    """
    Load settings from a configuration file (settings.txt).
    If the file is not found, it will use default settings.
    
    Returns:
        dict: A dictionary containing settings like risk caps.
    """
    settings = {}
    try:
        # Open and read the settings file
        with open("settings.txt", "r") as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    # Split the line into key and value and store in the settings dictionary
                    key, value = line.strip().split(":")
                    settings[key.strip()] = value.strip()
    except FileNotFoundError:
        print("settings.txt not found. Using default values.")
    return settings

def fetch_stock_info(ticker):
    """
    Fetch the sector and earnings date for a given stock ticker using Yahoo Finance.
    
    Args:
        ticker (str): The stock ticker (e.g., "AAPL").
    
    Returns:
        tuple: A tuple containing the sector (str) and earnings date (datetime or None).
    """
    try:
        stock = yf.Ticker(ticker)
        sector = stock.info.get('sector', 'Unknown')  # Default to 'Unknown' if not found
        
        # Extract earnings date from the calendar
        earnings_date = None
        calendar = stock.calendar
        if 'Earnings Date' in calendar and calendar['Earnings Date']:
            earnings_date = pd.to_datetime(calendar['Earnings Date'][0])
        
        return sector, earnings_date
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return 'Unknown', None  # Return 'Unknown' for sector if an error occurs

def process_risk_allocation(tickers, risk_cap):
    """
    Calculate risk allocation for a list of tickers, ensuring that no individual stock 
    exceeds the set risk cap per sector.
    
    Args:
        tickers (list): A list of stock tickers to process.
        risk_cap (float): The maximum allowable risk cap per sector (as a decimal).
    
    Returns:
        list: A list of dictionaries containing stock tickers, sectors, and calculated risk percentages.
    """
    data = []  # List to store data about tickers, sectors, and earnings dates
    
    # Fetch sector and earnings data for each ticker
    for ticker in tickers:
        sector, earnings_date = fetch_stock_info(ticker)
        data.append({
            'Ticker': ticker,
            'Sector': sector,
            'EarningsDate': earnings_date
        })
    
    # Convert data into a DataFrame for easier manipulation
    data = pd.DataFrame(data)
    
    # Filter out stocks with earnings in the next 7 days
    current_date = datetime.now()
    earnings_cutoff_date = current_date + timedelta(days=7)
    data['EarningsDate'] = pd.to_datetime(data['EarningsDate'], errors='coerce')
    data = data[(data['EarningsDate'].isna()) | (data['EarningsDate'] > earnings_cutoff_date)]
    
    # Group the data by sector to calculate risk per stock
    sector_groups = data.groupby('Sector')
    
    output = []  # List to store final output with risk allocations
    
    # Calculate risk allocation per stock within each sector
    for sector, group in sector_groups:
        num_stocks = len(group)  # Number of stocks in the sector
        risk_per_stock = min(risk_cap / num_stocks, risk_cap)  # Distribute the risk equally among stocks
        
        # Assign the calculated risk to each stock in the sector
        for _, row in group.iterrows():
            output.append({
                'Ticker': row['Ticker'],
                'Sector': sector,
                'RiskPercentage': round(risk_per_stock * 100, 2)  # Convert to percentage
            })
    
    return output

def format_output(output):
    """
    Format the calculated risk allocation output into a nicely structured string.
    
    Args:
        output (list): A list of dictionaries containing tickers, sectors, and risk percentages.
    
    Returns:
        str: A formatted string representing the risk allocation table.
    """
    formatted_output = "| Ticker | Sector                 | Risk %           |" + "\n"
    formatted_output += "|--------|------------------------|------------------|" + "\n"
    
    # Add each row of the output to the table
    for row in output:
        formatted_output += f"| {row['Ticker']:<6} | {row['Sector']:<22} | {row['RiskPercentage']:>15.2f}% |" + "\n"
    
    return formatted_output

def main():
    """
    Main function to load settings, fetch stock data, calculate risk allocation, 
    format the output, and save the results to a text file.
    """
    # Load the settings from the configuration file
    settings = load_settings()
    
    # Get the risk cap per sector (default is 2% if not specified)
    risk_cap_str = settings.get("risk_cap_per_sector", "2%")
    risk_cap = float(risk_cap_str.replace("%", "")) / 100  # Convert percentage to decimal
    
    # Load the tickers from the input.txt file
    with open("input.txt", "r") as file:
        tickers = file.read().strip().split(",")
    
    # Strip the exchange prefixes (e.g., NYSE:, NASDAQ:)
    tickers = [ticker.split(":")[-1] for ticker in tickers]
    
    # Process the risk allocation for the tickers
    output = process_risk_allocation(tickers, risk_cap)
    
    # Format the output into a table
    formatted_output = format_output(output)
    
    # Save the formatted output to a text file
    with open("output.txt", "w") as file:
        file.write(formatted_output)
    
    print("Success! Risk allocation by sector has been saved to 'output.txt'.")
    
    # Wait for user to press any key before closing the console
    input("Press any key to exit...")

# Run the main function if this script is executed
if __name__ == "__main__":
    main()