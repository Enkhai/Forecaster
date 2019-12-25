import requests

base_url = "http://api.openweathermap.org/data/2.5"
api_key = "8939087024a81b72f50fc697a216202d"

weather_suffix = "/weather"


def return_current_weather_data_by_city_name(city_name, country_code=None):
    url = base_url + weather_suffix
    q = city_name
    if country_code is not None:
        q += "," + country_code
    querystring = {"q": q, "APPID": api_key}

    response = requests.request("GET", url, params=querystring, timeout=3)
    return response.text


def return_current_weather_data_by_city_id(city_id):
    url = base_url + weather_suffix
    querystring = {"id": city_id, "APPID": api_key}

    response = requests.request("GET", url, params=querystring, timeout=3)
    return response.text


def return_current_weather_data_by_coords(lat, lon):
    url = base_url + weather_suffix
    querystring = {"lat": lat, "lon": lon, "APPID": api_key}

    response = requests.request("GET", url, params=querystring, timeout=3)
    return response.text


def return_current_weather_data_by_zip_code(zip_code, country_code=None):
    url = base_url + weather_suffix

    zip = zip_code
    if country_code is not None:
        zip += "," + country_code
    querystring = {"zip": zip, "APPID": api_key}

    response = requests.request("GET", url, params=querystring, timeout=3)
    return response.text
