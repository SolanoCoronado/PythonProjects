import requests
import json
from os.path import exists

# Function to fetch and cache exchange rates
def fetch_and_cache_exchange_rates(currency_code):
    try:
        response = requests.get(f"http://www.floatrates.com/daily/{currency_code}.json")
        response.raise_for_status()  # Raise an exception for HTTP errors
        exchange_data = response.json()
        with open(f'exchange_{currency_code}.json', 'w+', encoding='UTF-8') as json_file:
            json.dump(exchange_data, json_file)
        return exchange_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {currency_code}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {currency_code}: {e}")
        return None

# Pre-fetch and cache USD and EUR exchange rates
fetch_and_cache_exchange_rates("usd")
fetch_and_cache_exchange_rates("eur")

user_currency = input("Please type the currency you want to exchange: ").lower()
exchange_code = input("Please type the currency in which you want to obtain the value: ").lower()

while exchange_code:
    money_amount = input("Please enter the amount of money you have in your original currency: ")
    try:
        money_amount = float(money_amount)
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        continue

    print('Checking the cache...')
    if exists(f'exchange_{exchange_code}.json'):
        print('Oh! it is in the cache!')
        with open(f'exchange_{exchange_code}.json', 'r', encoding='UTF-8') as exchange_json:
            exchange_dict = json.load(exchange_json)
    else:
        print("Sorry, but it is not in the cache!")
        exchange_dict = fetch_and_cache_exchange_rates(exchange_code)
        if not exchange_dict:
            exchange_code = input("Please type another currency code or press Enter to exit: ").lower()
            continue

    if user_currency in exchange_dict:
        inverse_rate = exchange_dict[user_currency]["inverseRate"]
        exchanged_amount = round(money_amount * inverse_rate, 2)
        print(f'You received {exchanged_amount} {exchange_code.upper()}')
    else:
        print(f"Exchange rate for {user_currency} to {exchange_code} not found.")

    exchange_code = input("Please type another currency code or press Enter to exit: ").lower()

print("Exchanger program terminated.")
