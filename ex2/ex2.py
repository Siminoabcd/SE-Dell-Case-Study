import requests
import pandas as pd
from sqlalchemy import create_engine

def fetch_northern_european_countries():
    url = "https://restcountries.com/v3.1/subregion/Northern%20Europe"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None

def extract_country_info(country):
    official_name = country['name']['official']
    population = country.get('population', 'N/A')
    currency_code = next(iter(country.get('currencies', {})), None)
    currency_name = country.get('currencies', {}).get(currency_code, {}).get('name', 'N/A')
    return {'nation_official_name': official_name, 'currency_name': currency_name, 'population': population}

def load_dataframe_to_postgres(df, database, user, password, host='localhost', port='5432', table_name='country_data'):
    # Create a connection string
    conn_str = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    # Create a database engine
    engine = create_engine(conn_str)

    # Write the DataFrame to the PostgreSQL database
    df.to_sql(table_name, engine, if_exists='replace', index=False)

    print(f"DataFrame loaded into the table '{table_name}' in the '{database}' database.")

# Example usage:
data = fetch_northern_european_countries()

# Extract required information for each country
country_data = [extract_country_info(country) for country in data]

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(country_data)

# Define PostgreSQL connection parameters
DATABASE = "DellCaseStudy"
USER = "postgres"
PASSWORD = "**************"

# Load DataFrame into PostgreSQL
load_dataframe_to_postgres(df, DATABASE, USER, PASSWORD)
