def get_AIO_key():
    return b'your adafruit key'


def get_AIO_username():
    return 'yoru adafruit username'


def get_wifi_keys():
    return {b'your (basic) wifi SSID (name)': b'you (basic) wifi password',
            b'your (WPA2 Enterprise) wifi ssid here': (b"username here", b"password"), b'your wifi SSID': b'your password'}


def get_esp_id():
    return 1 # use for multiple esp32s

def get_firebase_endpoint():
    return "your streaming endpoint here, this is urequest.put(url) with the JSON data"