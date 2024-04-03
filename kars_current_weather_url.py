# Current Weather API url with the use of lat and lon in the url for more accurate result
# get lat and lon by calling geocoding_url function
# current weather api url
def current_weather_url():
   
    # get lat and lon by calling geocoding_url()
    lat, lon = geocoding_url()
 
    complete_current_weather_url = f"{OPENWEATHERMAP_API_URL}?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}"
    # print(complete_current_weather_url)
   
    response = requests.get(complete_current_weather_url)


    if response.status_code == 200:


        data = response.json()
        data = np.array(data)
     
        current_weather = data.item().get("main")
       
    else:
        print("Error:", response.status_code)


    return current_weather




current_weather = current_weather_url()
# print(current_weather)

