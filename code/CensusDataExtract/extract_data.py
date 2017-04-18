import time
import json
import numpy as np
import requests
from utils import get_geo_id, jsonp_res_to_obj
from config import THROTTLE, DECENNIAL_COLS, CENSUS_QUERY_URL

def get_census_data(lat, long, year='2010'):
    """
    Returns census data for a given coordinate (lat, long).
    :param lat: Latitude of point
    :param long: Longitude of point
    :param year: Year of the Decennial census. Default is 2010.
    :return: Census data for given point as a dict where key is the census data type and the value is the value of the 
    data.
    """
    geo_id = get_geo_id(lat, long)
    res = requests.get(CENSUS_QUERY_URL.format(geo_id[:2], geo_id[:11]))
    json_obj = jsonp_res_to_obj(res.text)
    row = {}
    for k, v in DECENNIAL_COLS.items():
        row[k] = json_obj['data'][year][v[0]][v[1]]
    return row

if __name__ == '__main__':
    lat = 40.767126
    long_start = -74.061684
    long_end = -74.161684
    for long in np.arange(-74.061684, -74.161684, -0.01):
        time.sleep(THROTTLE)
        data = get_census_data(lat, long)
        print data