VISUAL_CROSSING_API_KEY = 'PLEASE REGISTER YOUR API KEY'

def past_3(city,state):

    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    complete_url = f"{base_url}{city},{state}/last3days?unitGroup=us&key={VISUAL_CROSSING_API_KEY}"

    # print(complete_url)

    response = requests.get(complete_url)

    if response.status_code == 200:

        data = response.json()
        data = np.array(data)
      
        return(data) # returning everything, please let me know what you like to display

    else:
        print("Error:", response.status_code)

city = input("Enter City Name: ")
state = input("Enter State: ")
past_3_days_data = past_3(city, state)
print(past_3_days_data)
