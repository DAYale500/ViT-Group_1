# forecasting weather for the next 5 days
# Please let me know what data we want to display and I can work on extracting the result.
# for better view of the return result, please use this api url example: Atlanta, Georgia

# http://api.openweathermap.org/data/2.5/forecast?lat=33.7489924&lon=-84.3902644&appid=3bb060fc4c27204a5eb988afb0bf1101

def forecast_5_days():
   
    # get lat and lon by calling geocoding_url()
    lat, lon = geocoding_url()


    if (lat == False) and (lon == False):
        return "DATA NOT EXIST"


    # complete_current_weather_url = f"{OPENWEATHERMAP_API_URL}?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}"
    complete_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}"
    print(complete_url)
   
    response = requests.get(complete_url)


    if response.status_code == 200:


        data = response.json()
        data = np.array(data)
     
        return(data) # returning everything, please let me know what do you like to display


    else:
        print("Error:", response.status_code)


    # return current_weather




forecast_weather = forecast_5_days()
# print(forecast_weather)

