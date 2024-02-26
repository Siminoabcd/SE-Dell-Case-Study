""" 
All the values are imported manually just for the testing of the code.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Define the data
symbols = ['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A', 'APD', 'ABNB', 'AKAM', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ACGL', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK']
closing_values = ['92.58', '80.23', '119.46', '178.09', '377.32', '553.44', '176.52', '16', '80.41', '132.03', '232.79', '152.66', '108.17', '120.65', '119.28', '316.88', '129.09', '48.7', '159.13', '143.96', '145.29', '41.13', '174.99', '9.27', '71.6', '15.13', '82.45', '214.56', '71.32', '189.93', '118.96', '407.12', '178.2', '289.18', '107.47', '190.11', '340.89', '315.32', '30.03', '182.52', '197.16', '77.23', '87.29', '53.45', '267.66', '245', '178.37', '16.8', '113.69', '257.2']
moving_averages = [99.4, 73.16, 105.12, 148.97, 323.06, 535.66, 122.75, 18.16, 76.24, 122.1, 277.01, 132.45, 104.98, 168.03, 114.68, 292.54, 113.15, 50.93, 125.01, 132.16, 133.18, 42.78, 138.56, 9.53, 78.06, 14.35, 80.62, 168.91, 61.81, 189.16, 134.01, 344.74, 155.86, 261.91, 88.01, 183.87, 314.23, 321.05, 36.86, 183.73, 147.32, 92.59, 78.69, 73.16, 198.81, 227.51, 148.19, 15.71, 114.63, 217.95]

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
