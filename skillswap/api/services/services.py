import requests

def postal_to_latlng(postal_code, country="de"):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "postalcode": postal_code,
        "country": country,
        "format": "json"
    }

    res = requests.get(url, params=params, headers={
        "User-Agent": "SkillSwap"
    })

    data = res.json()
    if not data:
        return None, None

    return float(data[0]["lat"]), float(data[0]["lon"])
