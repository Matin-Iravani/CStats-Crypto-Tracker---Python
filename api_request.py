"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                              CStats API Runner File                              ║
║                                                                                  ║
║ This file is responsible for pulling cryptocurrency data from the CoinMarketCap  ║
║ API. It processes the response, handles any potential errors, and saves the      ║
║ fetched data to a local JSON file. Additionally, it saves the timestamp of when  ║
║ the data was last pulled.                                                        ║
║                                                                                  ║
║ Key features:                                                                    ║
║ - Pulls the latest cryptocurrency listings using CoinMarketCap's API.            ║
║ - Handles network issues such as connection errors, timeouts, and redirects.     ║
║ - Saves data to a JSON file with a timestamp of the last pull.                   ║
║ - Provides status messages based on success or failure of the API request.       ║
║                                                                                  ║
║ Error Codes:                                                                     ║
║  0: Success - Data was successfully pulled from the API and saved to the file.   ║
║  1: API Error - The API responded with an error (status code returned).          ║
║  2: Network Error - Could not reach the API due to a network issue (e.g.,        ║
║     connection error, timeout, or too many redirects).                           ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""


import json
from requests import Session
from datetime import datetime
from time_stamp import save_timestamp
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

def api_runner(file_path: str, active_message: list[str]):
    """
    Function to pull cryptocurrency data from CoinMarketCap API and handle errors.
    
    - file_path: Path to save the JSON data.
    - active_message: A list to store the status of the API request.
    """

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'  # API endpoint
    parameters = {
        'start': '1',     # Start at the first cryptocurrency at this rank
        'limit': '50',    # Limit to top 50 cryptocurrencies (NOTE YOU CAN CHANGE THIS VALUE BUT BE AWARE OF PULL CREDITS)
        'convert': 'USD'  # Convert prices to USD (NOTE YOU CAN CHANGE THE CURRENCY)
    }
    headers = {
        'Accepts': 'application/json',
        # API Key (Look at README.md to see how you can get your own for free!)
        'X-CMC_PRO_API_KEY': 'your-api-key',
    }
    
    session = Session() 
    session.headers.update(headers)
    
    try:
        # Make the API request
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        # Check if the API returned success
        if response.status_code == 200:
            # Add timestamp to data
            data['LastTimePulled'] = datetime.now().isoformat()
            
            # Save data to file
            save_timestamp()
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)  # Save the API data to a file with indent
            
            # Update the active_message to indicate success
            active_message[0] = 0
            active_message[1] = "Data pulled from API"
        
        else:
            # Handle case where API request failed
            active_message[0] = 1
            active_message[1] = response.status_code
    
    except ConnectionError:
        # Handle network-related errors
        active_message[0] = 2
        active_message[1] = "Network error. Please check your internet connection."
    
    except Timeout:
        # Handle request timeout errors
        active_message[0] = 2
        active_message[1] = "The request timed out. Please try again later."
    
    except TooManyRedirects:
        # Handle redirection errors
        active_message[0] = 2
        active_message[1] = "Too many redirects. Please check the URL."
    
    except Exception as e:
        # Catch any other unforeseen errors
        active_message[0] = 2
        active_message[1] = f"An error occurred: {str(e)}"


def pull_from_api(file_path: str, active_message: list[str]) -> None:
    """
    Pulls cryptocurrency data from the API and updates the local JSON file.

    This function interacts with the `api_runner` to pull the latest crypto data 
    and save it to the specified JSON file, either creating or overwriting the file. 
    If an error occurs during the pull, the status is reflected in `active_message`.
    """
    api_runner(file_path, active_message)