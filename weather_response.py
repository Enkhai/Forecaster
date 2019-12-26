import requests
from misc import is_number

base_url = "http://api.openweathermap.org/data/2.5"
api_key = "8939087024a81b72f50fc697a216202d"
units = "metric"

weather_suffix = "/weather"


# includes country code
def return_current_weather_data_by_city_name(city_name):
    url = base_url + weather_suffix
    querystring = {"q": city_name, "APPID": api_key, "units": units}

    response = requests.request("GET", url, params=querystring, timeout=3)
    return response.text


def return_current_weather_data_by_city_id(city_id):
    url = base_url + weather_suffix
    querystring = {"id": city_id, "APPID": api_key, "units": units}

    response = requests.request("GET", url, params=querystring, timeout=3)
    return response.text


def return_current_weather_data_by_coords(lon, lat):
    url = base_url + weather_suffix
    querystring = {"lon": lon, "lat": lat, "APPID": api_key, "units": units}

    response = requests.request("GET", url, params=querystring, timeout=3)
    return response.text


# includes country code
def return_current_weather_data_by_zip_code(zip_code):
    url = base_url + weather_suffix
    querystring = {"zip": zip_code, "APPID": api_key, "units": units}

    response = requests.request("GET", url, params=querystring, timeout=3)
    return response.text


def weather_response(request):
    split_request = request.split(',')
    response = None
    if len(split_request) == 2:
        if is_number(split_request[0]) and is_number(split_request[1]) and \
                -180 < float(split_request[0]) < 180 and -90 < float(split_request[1]) < 90:
            response = return_current_weather_data_by_coords(split_request[0], split_request[1])
        elif is_number(split_request[0]) and not is_number(split_request[1]):
            response = return_current_weather_data_by_zip_code(request)
        else:
            response = return_current_weather_data_by_city_name(request)
    elif len(split_request) == 1:
        if is_number(request):
            response = return_current_weather_data_by_zip_code(request)
            if len(response) < 15:
                response = return_current_weather_data_by_city_id(request)
        else:
            response = return_current_weather_data_by_city_name(request)

    return response
