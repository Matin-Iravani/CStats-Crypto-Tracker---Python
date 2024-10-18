from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
from time_stamp import save_timestamp

def api_runner(file_path: str, active_message: list[str]):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '11f8b595-67e7-4e34-8939-54154d879449',
    }
    
    session = Session()
    session.headers.update(headers)
    
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        # Check if the API returned success
        if response.status_code == 200:
            # Add timestamp to data
            data['LastTimePulled'] = datetime.now().isoformat()
            
            # Save data to file
            save_timestamp()
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            
            active_message[0] = 0
            active_message[1] = "Data pulled from API"
        
        else:
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

