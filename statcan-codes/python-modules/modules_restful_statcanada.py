"""Resful StatCanada

This code will extract inflation data for Telus SRM site market intelligence

Source of data is stat canada in: https://www.statcan.gc.ca/eng/developers/wds
Statcan contextual search: https://www150.statcan.gc.ca/n1/en/type/data
User guide can be found in: https://www.statcan.gc.ca/eng/developers/wds/user-guide
Concordance between CANSIM table number & Product ID:https://www.statcan.gc.ca/eng/developers/concordance
Consumer Price Index (CPI): https://www23.statcan.gc.ca/imdb/p2SV.pl?Function=getSurvey&SDDS=2301

the ``__doc__`` attribute. This is also what you'll see if you call
help() on a module or any other Python object.
"""
# [START import]
import json
import configparser
import requests     # using request for api calls
import yaml

from google.cloud import storage        # Import the Google Cloud client library 
# [END imports]

def get_statcan_api_config():
    # get url and header from config yaml
    with open('config.yaml', 'r') as yamlfile:
        config_data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    
    return config_data


# get the Series Data
def get_latestNperiod(payload):
    '''getDataFromCubePidCoordAndLatestNPeriods
    '''

    # get the configuraion parmaeters from config.yaml
    config_data = get_statcan_api_config()
    
    # get declared api-url-base
    api_url_base = config_data['STATCAN']['API_URL_BASE']

    # get universal header son that indicates response content type is json
    headers = config_data['STATCAN']['HEADERS']

    # add the api fucnation to the base url
    api_name = config_data['STATCAN']['LATEST_N_PERIOD']['API_NAME']
    api_url = api_url_base + api_name

    # get the series infro with post method
    response = requests.request("POST", api_url, headers=headers, data=payload)

    # https://docs.python.org/2.7/howto/unicode.html
    #print(response.text)
    data = json.loads(response.content[1:-1])
    response_body = json.dumps(data['object'])

    # check if there is an error
    if response.status_code == 200:
       return (response_body)
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

# get the Series Title info later to be used for chart titles
def get_getSeriesInfo():
    '''getSeriesInfoFromCubePidCoord
    '''

    # get the configuraion parmaeters form config.yaml
    config_data = get_statcan_api_config()
    
    # get declared api-url-base
    api_url_base = config_data['STATCAN']['API_URL_BASE']

    # get universal header son that indicates response content type is json
    headers = config_data['STATCAN']['HEADERS']

    # body of the post reques should include product id and coordinates
    productId = config_data['STATCAN']['SERIES_INFO']['ProductId']
    coordinate = config_data['STATCAN']['SERIES_INFO']['Coordinate']
    payload = json.dumps([{"productId": productId, "coordinate": coordinate}])   
 
    # add the api fucnation to the base url
    api_name = config_data['STATCAN']['SERIES_INFO']['API_NAME']
    api_url = api_url_base + api_name

    # get the series infro with post method
    response = requests.request("POST", api_url, headers=headers, data=payload)

    # https://docs.python.org/2.7/howto/unicode.html
    #print(response.text)
    data = json.loads(response.content[1:-1])
    response_body = json.dumps(data['object'])

    # check if there is an error
    if response.status_code == 200:
        return (response_body)
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None