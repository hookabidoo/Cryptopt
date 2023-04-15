from requests import Request, Session
import json
import fire 
import sys
import os


class Command(object):
    def __init__(self):
        self.session = Session()
        self.url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest' # Coinmarketcap API v2 to return the latest market quote for 1 or more cryptocurrencies.
        api_key = os.environ.get('API_KEY') # Get the API key from an environment variable
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key
        }
        
    def save(self, file_name, input_list):
        try:
            data = {} #create a dictionary to store the input list
            for item in input_list.split(','):
                key, value = item.split('=') # Split the item by '=' to extract the key and value when looping through the list 
                data[key] = float(value) # Convert the value to float and store it in the dictionary with the key
            with open(file_name, 'w') as json_file:
                json.dump(data, json_file, indent=4)            
            return(f'Saved to portfolio to {file_name}!')
        except Exception as e:
            print(f"Input with incorrect format entered. Make sure to enter a list of key-value pairs seperated by commas (e.g., BTC=3.3458,ETH=23.89347).")
            sys.exit(1)
        
        
    def show(self, file_path, currency_value):
        # Initialize total variable outside the loop
        total = 0
        
        #open JSON file
        try:
            with open(file_path, 'r') as file: 
                portfolio_data = json.load(file)
        except FileNotFoundError as e:
            # Handle the FileNotFoundError
            print(f"Error: {e}")
            print("Please input the right file path.")
            sys.exit(1)   
        
        #Fetch data from API
        response = self.session.get(self.url, params={'symbol': ','.join(portfolio_data.keys()), 'convert': currency_value}, headers=self.headers)
        # Check for API response errors
        if response.status_code != 200:
            print(f"Failed to fetch data. Error {response.status_code}: {response.text}")
            return None

        data = json.loads(response.text)
            
        # Get portfolio data from JSON file 
        for key, amount_owe in portfolio_data.items():      
            try:
                # retrive cryptocurrency symbol and price returned from API response
                symbol = data['data'][key][0]['symbol']
                price = data['data'][key][0]['quote'][currency_value]['price']
                value = float(price) * float(amount_owe) # Calculating the value of the coins in the chosen currency
                value_string = '{:,}'.format(round(value, 2)) # Formatting the value to 2 decimal places
                print(symbol, value_string) 
                total += value # Add the value to the total
                  
            except Exception as e:
                # Handle other exceptions as needed
                print(f"Incorrect value detected: {e}. Please enter correct input list to portfolio OR enter correct currency value to the command.")
                sys.exit(1)    
            
        return(f'Sum of all cryptocurrency holdings is : {total} {currency_value}!') 

if __name__ == '__main__':
    fire.Fire(Command)
    