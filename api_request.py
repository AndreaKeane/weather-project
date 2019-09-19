#!/usr/bin/env python3
from configparser import ConfigParser
from datetime import date, datetime, timedelta
import requests
import sqlalchemy as sa
import json 

def main():
    ''' '''
    # Retrieve private variables from config 
    config = ConfigParser()
    config.read('private_config.ini')

    # Connect to MySQL database, with parameters provided in config
    connection = get_db_connection(config)
    start_date = date(2018, 1, 1)
    end_date = date.today()
    for single_date in daterange(start_date, end_date):
        response = make_request(api_key=config['darksky']['api_key'], 
                            latitude='43.0972', 
                            longitude='89.5043', 
                            connection=connection,
                            time=single_date.strftime("%Y-%m-%dT00:00:00"),
                            )
   
    
def make_request(api_key, latitude, longitude, time=None, connection=None):
    ''' 
    Setup API Request, https://darksky.net/dev/docs
        https://api.darksky.net/forecast/[key]/[latitude],[longitude],[time]
        The latitude of a location (in decimal degrees). Positive is north, negative is south.
        The longitude of a location (in decimal degrees). Positive is east, negative is west.
        Either be a UNIX time or a string formatted
    ''' 
    # Make Request
    if time: 
        url_template = f'https://api.darksky.net/forecast/{api_key}/{latitude},{longitude},{time}'
    else: 
        url_template = f'https://api.darksky.net/forecast/{api_key}/{latitude},{longitude}'
    
    # Make request
    response = requests.get(url_template)

    # Handle Response 
    # TODO: something more useful, raise errors
    if response.status_code == 200:
        # print('Success!')
        if connection: 
            # Retrieve the json part of the response
            # The default string interpolation returns single-quote JSON, MySQL needs double-quotes in the JSON string
            json_result = json.dumps(response.json())
            connection.execute(f"REPLACE INTO requests (latitude, longitude, time, response) VALUES ({latitude}, {longitude}, NULLIF('{time}', 'None'), '{json_result}');")
    else: 
        print("ERROR")
        print(response.status_code)
    return response


def get_db_connection(config):
    '''Create and return a connection to the database specified by config'''
     # Setup database connection 
    user = config['database']['user']
    pswd = ''
    host = config['database']['host']
    port = config['database']['port']
    db = config['database']['db']

    engine = sa.create_engine(f'mysql+mysqlconnector://{user}:{pswd}@{host}:{port}/{db}')
    return engine.connect()


def daterange(start_date, end_date):
    '''
    Generator function to iterate over a range of dates
    Ref: https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
    '''
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


if __name__ == "__main__":
    main()