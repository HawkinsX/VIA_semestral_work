import urllib.request
import json


with urllib.request.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=germany") as url:
    data = json.loads(url.read().decode())
    print(data["results"]["geometry"])