import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Scrape the S&P500 companies table from the given URL and extract ticker symbols.
def scrape_sp500_tickers(num_companies=50):

    # URL of the Wikipedia page
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the list of S&P500 companies
    table = soup.find('table', {'class': 'wikitable sortable'})

    # Initialize an empty list to store ticker symbols
    ticker_symbols = []

    # Extract ticker symbols from the table
    for row in table.find_all('tr')[1:]:  # Skip the header row
        ticker = row.find_all('td')[0].text.strip()  # Ticker symbol is in the first column
        ticker_symbols.append(ticker)

        # Break the loop if desired number of companies is reached
        if len(ticker_symbols) >= num_companies:
            break

    return ticker_symbols


# Get the last closing value for each company in the list of ticker symbols.
def last_closing_value(symbols):
    closing_values = []

    for symbol in symbols:
        # Construct the URL for Yahoo Finance
        url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}&tsrc=fin-srch"

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            try:
                # Find the element containing the previous close value
                prev_close_element = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'})

                # Extract the previous close value
                prev_close = prev_close_element['value']

                # Append symbol and previous close value to the list
                closing_values.append(prev_close)
            except Exception as e:
                print(f"Error processing data for {symbol}: {e}")
        else:
            print(f"Failed to fetch data for {symbol}")

    return closing_values


def moving_average(symbols):
    moving_averages = []

    # Configure Selenium to use a headless browser
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    for symbol in symbols:
        try:
            # Construct the URL for Yahoo Finance
            url = f"https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}"

            # Navigate to the URL
            driver.get(url)

            # Wait for the 200-Day Moving Average data to be visible
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='200-Day Moving Average']")))

            # Find the element containing the 200-Day Moving Average value
            ma_element = driver.find_element(By.XPATH, "//span[text()='200-Day Moving Average']/parent::td/following-sibling::td")
            ma_value = ma_element.text.strip()

            # Append the moving average value to the list
            moving_averages.append(float(ma_value))
        except Exception as e:
            print(f"Error processing data for {symbol}: {e}")
            moving_averages.append((symbol, None))

    # Close the Selenium WebDriver
    driver.quit()

    return moving_averages

# Get all values
symbols = scrape_sp500_tickers()
closing_values = last_closing_value(symbols)
moving_averages = moving_average(symbols)

# Create DataFrame
df = pd.DataFrame({'symbol': symbols, 'closing_value': closing_values, 'moving_average': moving_averages})

# Convert closing_value and moving_average to numeric
df['closing_value'] = pd.to_numeric(df['closing_value'])
df['moving_average'] = pd.to_numeric(df['moving_average'])

# Create is_cheap column
df['is_cheap'] = df['closing_value'] < df['moving_average']


# Filter the DataFrame for companies where is_cheap is True
cheap_companies = df[df['is_cheap']]

# Plotting
plt.figure(figsize=(12, 6))
plt.bar(cheap_companies['symbol'], cheap_companies['closing_value'], color='green')
plt.xlabel('Ticker Symbol')
plt.ylabel('Previous Close Value')
plt.title('Previous Close Value of Cheap Companies')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

