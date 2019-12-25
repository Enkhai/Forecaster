import time
import requests
import os

mappings = {
    "200": "11d", "201": "11d", "202": "11d", "210": "11d", "211": "11d", "212": "11d", "221": "11d", "230": "11d",
    "231": "11d", "232": "11d",
    "300": "09d", "301": "09d", "302": "09d", "310": "09d", "311": "09d", "312": "09d", "313": "09d", "314": "09d",
    "321": "09d",
    "500": "10d", "501": "10d", "502": "10d", "503": "10d", "504": "10d", "511": "13d", "520": "09d", "521": "09d",
    "522": "09d", "531": "09d",
    "600": "13d", "601": "13d", "602": "13d", "611": "13d", "612": "13d", "613": "13d", "615": "13d", "616": "13d",
    "620": "13d", "621": "13d", "622": "13d",
    "701": "50d", "711": "50d", "721": "50d", "731": "50d", "741": "50d", "751": "50d", "761": "50d", "762": "50d",
    "771": "50d", "781": "50d",
    "800": ["01d", "01n"],
    "801": ["02d", "02n"], "802": ["03d", "03n"], "803": ["04d", "04n"], "804": ["04d", "04n"]
}

base_url = "http://openweathermap.org/img/wn/"
suffix = "@2x.png"

directory = os.path.join(os.getcwd(), "icons\\weather\\")


def map_weather_code_to_image_path(code, sunrise, sunset):
    icon = mappings[code]
    sysdate = int(time.time())
    if type(icon) == list:
        if sunrise < sysdate < sunset:
            image_path = directory + icon[0] + suffix
        else:
            image_path = directory + icon[1] + suffix
    else:
        image_path = directory + icon + suffix
    return image_path


def get_all_images():
    unique_images = set()
    for val in mappings.values():
        if type(val) == list:
            for v in val:
                unique_images.add(v)
        else:
            unique_images.add(val)
    for image in unique_images:
        if type(image) == list:
            for i in image:
                url = base_url + i + suffix
                icon_image = requests.get(url)
                with open(directory + i + suffix, 'wb') as f:
                    f.write(icon_image.content)
        else:
            url = base_url + image + suffix
            icon_image = requests.get(url)
            with open(directory + image + suffix, 'wb') as f:
                f.write(icon_image.content)


if __name__ == '__main__':
    # get_all_images()
    pass
