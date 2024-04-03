# I noticed that many API URLs need latitude and longitude.
# So, I made a function to get these. I'll work on other APIs
# later today. When we use just a city name in an API URL, it
# can be tricky if there are cities with the same name in
# different states. That's why using latitude and longitude is
# better.


import numpy as np
import requests




# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key. You will have to sign up and get your own key (visit the link below)
OPENWEATHERMAP_API_KEY = '3bb060fc4c27204a5eb988afb0bf1101'
OPENWEATHERMAP_API_URL = 'http://api.openweathermap.org/data/2.5/weather'


# GEOCODING API URL
def geocoding_url ():
    city = input("Enter City Name: ")
    state = input("Enter State: ")
    # state = state.lower()


    geocoding_base_url = 'http://api.openweathermap.org/geo/1.0/direct?q='
    # complete_geocoding_url = geocoding_base_url + city + ',' + state + '&limit=5&appid=' + OPENWEATHERMAP_API_KEY
    complete_geocoding_url = f"{geocoding_base_url}{city},{state}&limit=5&appid={OPENWEATHERMAP_API_KEY}"
    print(complete_geocoding_url)
   
    response = requests.get(complete_geocoding_url)


    if response.status_code == 200:
       
        data = response.json()
        data = np.array(data)
        # print(data)


        state_index = 0
        city_found = False
        state_found = False


        for index, item in enumerate(data):
            if (item.get('name')).lower() == city.lower():
                city_found = True


            if (item.get('state')).lower() == state.lower():
                state_index = index
                state_found = True
                break
    else:
        print("Error:", response.status_code)


    if (city_found == True) and (state_found == True):
        lat = data[state_index]['lat']
        lon = data[state_index]['lon']
        print(f"lat {lat}, lon {lon}")
        return lat, lon
    else:
        print("DATA NOT FOUND")
        sys.exit() #terminate the app




