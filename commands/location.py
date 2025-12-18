import requests

COUNTRY_MAP = {
    "IN": "India"
}

def get_location(raw=False):
    r = requests.get("https://ipinfo.io/json", timeout=5)
    data = r.json()

    city = data.get("city")
    region = data.get("region")
    country_code = data.get("country")

    print("DEBUG LOCATION:", city, region, country_code)  # 👈 TEMP DEBUG

    country = COUNTRY_MAP.get(country_code, country_code)

    if raw:
        return city, region, country

    return f"You are currently in {city}, {region}, {country}."





# import requests

# def get_location():
#     try:
#         r = requests.get("https://ipinfo.io/json", timeout=5)
#         data = r.json()
#         return f"You are currently in {data['city']}, {data['region']}, {data['country']}."
#     except:
#         return "I could not determine your location."
