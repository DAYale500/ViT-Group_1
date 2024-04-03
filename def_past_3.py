# Thanks, Geoffrey for finding the weather api (visualcrossing.com)
# that would work for us today. We had the AQI and Past 3 Days’
# Historical Data API work and running. Here is the API function
# that I posted in chat today.

def past_3(city,state):


    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    complete_url = f"{base_url}{city},{state}/last3days?unitGroup=us&key={OPENWEATHERMAP_API_KEY}"


    # print(complete_url)


    response = requests.get(complete_url)


    if response.status_code == 200:


        data = response.json()
        data = np.array(data)

        return(data) # returning everything, please let me know what do you like to display


    else:
        print("Error:", response.status_code)





Weather API Sites

https://www.visualcrossing.com/weather-api?ga_api20&gad_source=1&gclid=CjwKCAjwtqmwBhBVEiwAL-WAYb7EziwqjGrHkepnCzxQ1ECm88VLki5nX8nsu4oPCtSakFhkaxtoahoCsewQAvD_BwE

Past 3 Days
https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/London,UK/last3days?unitGroup=us&key=KCSKHXP2N9LN2JEVXHEWVMASV

https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Atlanta,GA/last3days?unitGroup=us&key=KCSKHXP2N9LN2JEVXHEWVMASV


https://www.meteosource.com/air-quality-api
https://www.meteosource.com/pricing

Historical and Air Pollution not free

https://open-meteo.com/en/docs/air-quality-api

