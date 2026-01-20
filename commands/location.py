import requests

def get_location():
    try:
        data = requests.get("https://ipinfo.io/json", timeout=5).json()

        loc = data.get("loc")  # "lat,long"
        if not loc:
            return "I could not determine your location."

        lat, lon = loc.split(",")

        geo = requests.get(
            f"https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": lat,
                "lon": lon,
                "format": "json"
            },
            headers={"User-Agent": "jarvis"}
        ).json()

        address = geo.get("address", {})
        city = address.get("city") or address.get("town") or address.get("village")
        state = address.get("state")
        country = address.get("country")

        return f"You are approximately in {city}, {state}, {country}."

    except:
        return "I could not determine your location."
