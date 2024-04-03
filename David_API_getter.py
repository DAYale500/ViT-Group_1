# import in the two modules for making API calls and parsing the data
import json
import requests


def main():
    # set a url variable with the URL using David's API key:
    # lat= 44.34, lon=10.99
    # this can be converted to a sys.argv() input that will need to be cleaned in the Tkinter area
    url_weather = "https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=29b6f476ddbbec25a80a7d86634f3399"
    weather = get_weather(url_weather) # send API response for preparation
    print_outs(weather)  # this runs the print_out of all those in the API return


def get_weather(url_weather):
    # set a variable response to the "get" request of the url
    response = requests.get(url_weather)  # get the information form the website

    # print to verify we have a status code of 200
    print(response, "\n")

    # assign a variable json_data to the responses' json
    json_data = response.json()  # returns a string that still needs to be deserialized

    # lets make it into a python dictionary by using the appropriate json method
    return json.loads(response.text)  # this might be redundant.


def print_outs(weather):
    print(f"Place: {weather['name']}, {weather['sys']['country']}")  # units?
    print(f"Lat: {weather['coord']['lon']}, Lon: {weather['coord']['lon']}")
    print()
    print(f"Temp: {weather['main']['temp'] - 273.15:.1f}C, but feels like: {weather['main']['feels_like'] - 273.15:.1f}C")
    print(f"Temp min/max: {weather['main']['temp_min'] - 273.15:.1f}/{weather['main']['temp_max'] - 273.15:.1f}C")
    print(f"Humidity: {weather['main']['humidity']}%")
    print()
    print(f"Pressure: {weather['main']['pressure']}")
    print(f"Pressure @ seal level: {weather['main']['sea_level']} mbars")
    print(f"Pressure @ ground level: {weather['main']['grnd_level']}  mbars")
    print(f"Pressure: {weather['main']['pressure']} mbars")
    print()
    print(f"Clouds: {weather['weather'][0]['description']}")
    print(f"visibility: {weather['visibility']} meters")  # units?
    print()
    # this will convert wind angle to a cardinal direction
    wind_angle = weather["wind"]["deg"]
    wind_card = convert_wind(wind_angle)
    print(f"Wind speed: {weather['wind']['speed']} m/s, from the {wind_card}, with gusts to {weather['wind']['gust']} m/s")  # units?


def convert_wind(wind_angle):
    # Define the mapping of ranges to cardinal direction names
    # Each range covers 45 degrees since 360 / 8 directions = 45 degrees each
    # The range is adjusted by 22.5 degrees to center the direction in the middle of its range
    directions = [
        (337.5, 360, "N"),
        (0, 22.5, "N"),
        (22.5, 67.5, "NE"),
        (67.5, 112.5, "E"),
        (112.5, 157.5, "SE"),
        (157.5, 202.5, "S"),
        (202.5, 247.5, "SW"),
        (247.5, 292.5, "W"),
        (292.5, 337.5, "NW"),
    ]
    # Find and return the direction name
    for start, end, name in directions:
        if start <= wind_angle < end:
            return name
    return "Unknown"  # In case the number doesn't match any range


if __name__ == "__main__":
    main()
