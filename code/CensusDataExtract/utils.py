import json
import requests
from config import CENSUS_BLOCK_CONV_URL


def get_geo_id(lat, long):
    """
    Returns the GEO_ID aka FIPS code of the point given by a latitude and longitude.
    :param lat: Latutude of the point 
    :param long: Longitude of the point
    :return: FIPS code or GEO_ID of the point
    """
    res = requests.get(CENSUS_BLOCK_CONV_URL.format(lat, long))
    return res.json()['Block']['FIPS']


def jsonp_res_to_obj(jsonp_res):
    """
    Converts a jsonp response to a python dict by stripping off the jsonp call from the response.
    :param jsonp_res: JSONP response as a string
    :return: Python dict of the response
    """
    open_parens_idx = jsonp_res.index('(')
    json_str = jsonp_res[open_parens_idx + 1: -1]
    json_obj = json.loads(json_str)
    return json_obj
