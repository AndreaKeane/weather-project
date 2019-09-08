#!/usr/bin/env python3
from configparser import ConfigParser
from datetime import date, datetime
import requests

def main():
    ''' '''
    # Retrieve private variables from config 
    config = ConfigParser()
    config.read('private_config.ini')

    # Setup API Request
    api_key = config['darksky']['api_key']
    latitude = '43.0972'
    longitude = '89.5043'

    response = make_request(api_key, latitude, longitude)
    print_response(response)

    
def make_request(api_key, latitude, longitude):
    ''' ''' 
    # Make Request
    response = requests.get(f'https://api.darksky.net/forecast/{api_key}/{latitude},{longitude}')

    # Handle Response 
    # TODO: something more useful, raise errors
    if response.status_code == 200:
        print('Success!')
    else: 
        print("ERROR")
        print(response.status_code)
    return response

def print_response(response):
    '''Temporary method to re-create original behavior''' 
    for item in response: 
        print(item)

if __name__ == "__main__":
    main()