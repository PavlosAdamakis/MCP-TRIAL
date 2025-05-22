import requests

def run_weather_tool(params: dict) -> str:
    city = params.get("city", "Copenhagen")
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        return response.text.strip()
    except Exception as e:
        return f" Failed to get weather: {e}"
