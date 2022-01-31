import requests
import json
import pycountry


def get_country(ip):
    endpoint = f'https://ipinfo.io/{ip}/json'
    response = requests.get(endpoint, verify = True)

    if response.status_code != 200:
        return 'Status:', response.status_code, 'Problem with the request. Exiting.'
        exit()

    data = response.json()
    return data['country']

def get_location(request):
    import urllib.request
    from requests import get
    device = request.META.get('GDMSESSION')
    device_full = request.META.get('HTTP_USER_AGENT')
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    my_country = get_country(external_ip)
    c = pycountry.countries.get(alpha_2=my_country)
    return device, device_full, c
