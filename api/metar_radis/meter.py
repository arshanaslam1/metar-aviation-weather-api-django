import json
import urllib3
import traceback
from .settings import METAR_ENDPOINT, redis_instance
from .metar import Metar


def get_station_report(scode, nocache=0):
    processed_metar_res = dict()
    if nocache == 0:
        processed_metar_res = get_cached_response(scode)
    if nocache == 1 or len(processed_metar_res) == 0:
        station_endpoint = METAR_ENDPOINT + '/stations/{scode}.TXT'.format(scode=scode)
        http = urllib3.PoolManager()
        metar_sresp = http.request('GET', station_endpoint)
        if metar_sresp.status == 404:
            processed_metar_res = {
                'message': 'No such station code found - %s' % scode,
                'status': 'success',
                'code': 1404
            }
        else:
            processed_metar_res = process_metar_response(metar_sresp.data.decode('utf-8'))
            # Update cache
            encache_response(processed_metar_res)
    # return processed_metar_res
    return processed_metar_res


def process_metar_response(metar_resp):
    """
    Process the response received from metar_radis and returns the JSON data in following format -
    {
    'data': {
            'station': 'KSGS',
            'ast_observation': '2017/04/11 at 16:00 GMT',
            'temperature': '-1 C (30 F)',
            'wind': 'S at 6 mph (5 knots)'
        }
    }
    :param metar_resp:
    :return: Processed metar_radis response in JSON format
    """
    if not metar_resp:
        return {"message": "No response received from metar_radis"}

    # Sample response sent by metar_radis -
    # 2017/11/25 18:33 KSGS 251833Z AUTO 29006KT 10SM CLR 04/M06 A3009 RMK AO2 T00381061
    try:
        metar_resp = metar_resp.split("\n")
        metar_attrs = metar_resp[1]
        metar_data = Metar.Metar(metar_attrs)
        metar_data_json = metar_data.json_report()

        return metar_data_json
    except Exception as ex:
        traceback.print_exc()
        return {"message": "Error occurred while parsing the metar_radis response", "response": metar_resp}


def encache_response( processed_metar_res, ttl=300):
    """
    Caches the station report with expiry(ttl), where redis key is station code.
    :param processed_metar_res: Station weather report to be cached.
    :param ttl: Time to live
    """
    #redis_connection.setex(name=processed_metar_res['station'], value=jsonify(processed_metar_res), time=ttl)
    data = json.dumps(processed_metar_res)
    redis_instance.set(processed_metar_res['station'], data, ex=ttl)


def get_cached_response(scode):
    """
    Fetches the cached report for the station.
    :param scode: Station code
    :param asjson:
    :return: Cached report either in json(string) or as dictionary depending upon `asjson` attribute.
    """
    value = redis_instance.get(scode)
    try:
        value = json.loads(value.decode('utf-8'))
    except:
        value = ""
    return value





