import json
import requests
from config import CENSUS_BLOCK_CONV_URL, COUNTY_CODES


def get_geo_id(lat, long):
    """
    Returns the GEO_ID aka FIPS code of the point given by a latitude and longitude.
    :param lat: Latutude of the point 
    :param long: Longitude of the point
    :return: FIPS code or GEO_ID of the point
    """
    res = requests.get(CENSUS_BLOCK_CONV_URL.format(lat, long))
    return res.json()['Block']['FIPS'][:11]


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


def cols_config_to_csv_tables(cols_config):
    """
    Converts a config object for columns to a comma separated string of tables.
    :param cols_config: Config object for a single column. (See config.py)
    :return: Comma separated string of tables
    """
    tables = [v[0] for k, v in cols_config.items()]
    return ','.join(tables)


def geo_id_to_cenrep_geo_id(geo_id):
    """
    Converts a normal GEO_ID to a format that works with the census reporter API.
    :param geo_id: A valid GEO_ID (FIPS)
    :return: GEO_ID in a format supported by census reporter API
    """
    return '14000US{}'.format(geo_id)


def is_inside_county(lat, long, counties=COUNTY_CODES):
    geo_id = get_geo_id(lat, long)
    county_id = str(geo_id[2:5])
    is_inside = False
    for k, v in counties.items():
        if v == county_id:
            is_inside = True
            break
    return is_inside