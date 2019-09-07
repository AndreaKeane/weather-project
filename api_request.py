from datetime import date, datetime
import requests
import sys


def main():
    ''' '''

    # Setup API Request
    api_key = '3060db5bb79c7111e2d1a9843f02a8ac'
    latitude = 43.0972
    longitude = 89.5043

    # Create URL template
    response = requests.get(f'https://api.darksky.net/forecast/{api_key}/{latitude},{longitude}')

    if response.status_code == 200:
        print('Success!')
    else: 
        print("ERROR")
        print(response.status_code)
        sys.exit()

    for item in response: 
        print(item)

if __name__ == "__main__":
    main()