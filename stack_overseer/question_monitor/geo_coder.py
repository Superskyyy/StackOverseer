"""
A utility to call geo_coder APIs
Change the url_constructor if a new geo_coder api is used

"""
import json
import time
from urllib.parse import quote

import requests

from stack_overseer.question_monitor.config.api_config import GEO_CODER_API, GEO_CODER_API_ENDPOINT


def geo_coder(address: str):
    # constructs url
    url = GEO_CODER_API_ENDPOINT + quote(address) + ".JSON?key=" + GEO_CODER_API
    try:
        time.sleep(0.1)
        result = requests.get(url)
    except:  # bad request
        return ("-1", "-1")

    def jsonify(raw_result):
        # decode the results to unicode
        cleaned = raw_result.decode('utf8')
        # load to json format
        data = json.loads(cleaned)

        return data

    cleaned = jsonify(result.content)

    try:
        geo_code = cleaned["results"][0]['position'] if len(cleaned["results"]) > 0 else {'lat': -1, 'lon': -1}
    except Exception as e:  # http 404
        return ("-1", "-1")
    geo_tuple = (str(geo_code['lat']), str(geo_code['lon']))
    return geo_tuple


# simple test
if __name__ == "__main__":
    foo = geo_coder("Reading, United Kingdom")
    print(foo)
