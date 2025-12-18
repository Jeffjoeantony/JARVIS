import requests

API_KEY = "d9bc1a13c2ef820c15ea7068ae155963"

def get_weather(city):
    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("cod") != 200:
            return None

        temp = round(data["main"]["temp"])
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        return (
            f"The current temperature is {temp} degrees Celsius "
            f"with {desc}. Humidity is {humidity} percent."
        )

    except:
        return None
