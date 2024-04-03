import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime
from datetime import datetime, timedelta
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL library
import pytz  # Import pytz for timezone handling
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np








# Mapping of US state abbreviations to full names




us_states = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}








# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
api_key = "29b6f476ddbbec25a80a7d86634f3399"


api_key_visualcrossing = "9LMZ7SVJRRQN9QQ4XCHK46VBN"












class WeatherApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Weather App")
        self.window.geometry("600x400")




        self.location_var = tk.StringVar()
        self.temperature_unit = tk.StringVar(value="metric")
       
        self.quote_of_the_day = self.get_quote_of_the_day()




       # Configure ttk Style for cyberpunk theme
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as a base
        self.style.configure('.', foreground='cyan', background='black')  # Set foreground and background colors for all widgets
        self.style.map('.', foreground=[('disabled', 'gray')])  # Set disabled widget color to gray




        # Customize specific widget elements for cyberpunk theme
        self.style.configure('TButton', foreground='cyan', background='black', font=('Arial', 12, 'bold'))
        self.style.map('TButton', foreground=[('active', 'orange')])  # Set active button color to orange
        self.style.configure('TLabel', foreground='cyan', background='black', font=('Arial', 12, 'bold'))
        self.style.configure('TEntry', foreground='cyan', background='black', font=('Arial', 10))
        self.style.configure('TRadiobutton', foreground='cyan', background='black', font=('Arial', 10))




        # Display the quote of the day and international holiday in the GUI
        self.display_quote()


        # Start the GUI event loop
        self.init_page()




    def get_quote_of_the_day(self):
        # Example API endpoint for getting a quote of the day
        quote_api_url = "https://zenquotes.io/api/quotes"
        response = requests.get(quote_api_url)
        if response.status_code == 200:
            quote_data = response.json()
            return quote_data[random.choice(range(0,len(quote_data)-1))]['q']
        return "Have a nice day!"




    def display_quote(self):
        # Display the quote of the day and international holiday in the GUI
        quote_label = ttk.Label(self.window, text="A Quote to Live By", font=("Arial", 12, "bold"), justify="center")
        quote_label.pack()
        quote_entry = ttk.Entry(self.window, width=len(self.quote_of_the_day)+10, font=("Arial", 10), justify="center")
        quote_entry.insert(0, self.quote_of_the_day)
        quote_entry.config(state="readonly")
        quote_entry.pack()




    def sanitize_user_input(self, user_input):
        city_name = ""
        state_code = ""
        country_code = ""




        # Check if User Input is Single Word
        if "," not in user_input:
            city_name = user_input.lower().title()
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
            return [city_name, geocoding_url]




        # Check if User Input is Multiple Words
        if "," in user_input:
            user_input_parts = [x.strip() for x in user_input.split(",")]
            if len(user_input_parts) == 2:
                if user_input_parts[1].upper() in us_states:
                    city_name = user_input_parts[0].lower().title()
                    state_code = us_states[user_input_parts[1].upper()]
                    country_code = "US"
                    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit=1&appid={api_key}"
                    return [city_name, geocoding_url]
                else:
                    city_name = user_input_parts[0].lower().title()
                    country_code = user_input_parts[1]
                    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=1&appid={api_key}"
                    return [city_name, geocoding_url]
            elif len(user_input_parts) == 3:
                city_name = user_input_parts[0].lower().title()
                state_code = us_states[user_input_parts[1].upper()]
                country_code = user_input_parts[2]
                geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit=1&appid={api_key}"
                return [city_name, geocoding_url]




        return None  # Invalid input format




    def get_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
       
    def past_3(self, city, state):
        base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        complete_url = f"{base_url}{city},{state}/last3days?unitGroup=us&key={api_key_visualcrossing}"
        print(complete_url)


        # Use get_data method to fetch data
        data = self.get_data(complete_url)


        if data:
            data = np.array(data)


            # You can process and display this data as needed
            print("Past 3 days weather data:", data)
        else:
            print("Error: Failed to fetch data from API.")
       
    def create_air_quality(self, city_name):
        # Get data from API using the WeatherApp's get_data method
        api_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}?unitGroup=metric&key=9LMZ7SVJRRQN9QQ4XCHK46VBN&contentType=json&elements=datetime,pm1,pm2p5,pm10,o3,no2,so2,co,aqius,aqieur"
        data = self.get_data(api_url)




        if data:
            # Process data
            df = pd.DataFrame(data["days"])




            # Plotting AQI over time
            plt.figure(figsize=(10, 6))
            plt.plot(df["datetime"], df["aqius"], label="AQI (US)")
            plt.xlabel("Date")
            plt.ylabel("AQI")
            plt.title("Air Quality Index (AQI) in " + city_name)
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            self.popupmsg("Error", "Failed to fetch data from API.")


    def display_air_quality(self):
        city_name = self.location_var.get()
        if city_name:
            self.create_air_quality(city_name)
        else:
            self.popupmsg("Error", "Please enter a valid city name.")


    def fetch_current_weather(self):
        user_input = self.location_var.get()
        sanitized_input = self.sanitize_user_input(user_input)
        if sanitized_input:
            city_name, geocoding_url = sanitized_input
            geocode_data = self.get_data(geocoding_url)
            if geocode_data:
                lat = str(round(geocode_data[0]["lat"], 5))
                lon = str(round(geocode_data[0]["lon"], 5))
                current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={self.temperature_unit.get()}"
                current_weather_data = self.get_data(current_weather_url)
                if current_weather_data:
                    self.display_current_weather(current_weather_data, city_name)
                else:
                    self.popupmsg("Error", "Weather data not available.")
            else:
                self.popupmsg("Error", "Geocode data not available.")
        else:
            self.popupmsg("Error", "Invalid input format.")








    def fetch_5_day_forecast(self):
        user_input = self.location_var.get()
        sanitized_input = self.sanitize_user_input(user_input)
        if sanitized_input:
            city_name, geocoding_url = sanitized_input
            geocode_data = self.get_data(geocoding_url)
            if geocode_data:
                lat = str(round(geocode_data[0]["lat"], 5))
                lon = str(round(geocode_data[0]["lon"], 5))
                forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units={self.temperature_unit.get()}"
                forecast_data = self.get_data(forecast_url)
                if forecast_data:
                    self.display_5_day_forecast(forecast_data, city_name)
                else:
                    self.popupmsg("Error", "Forecast data not available.")
            else:
                self.popupmsg("Error", "Geocode data not available.")
        else:
            self.popupmsg("Error", "Invalid input format.")








    def display_current_weather(self, data, city_name):
        window = tk.Toplevel()
        window.title(f"Current Weather in {city_name}")




        weather_condition = data["weather"][0]["main"].lower()  # Ensure lowercase for matching
       
        weather_label = ttk.Label(window, text="Weather:", font=("Arial", 12, "bold"), justify="center")
        weather_label.pack()




        weather_data_text = f'{data["weather"][0]["main"]}, {data["weather"][0]["description"]}'
        weather_data_entry = ttk.Entry(window, width=len(weather_data_text) + 10, font=("Arial", 10), justify="center")
        weather_data_entry.insert(0, weather_data_text)
        weather_data_entry.config(state="readonly")
        weather_data_entry.pack()








        temp_unit = "°C" if self.temperature_unit.get() == "metric" else "°F"








        main_temp_label = ttk.Label(window, text="Main Temperature:", font=("Arial", 12, "bold"), justify="center")
        main_temp_label.pack()
        main_temp_data_text = f"{data['main']['temp']} °C" if self.temperature_unit.get() == "metric" else f"{data['main']['temp']} °F"
        main_temp_data_entry = ttk.Entry(window, width=len(main_temp_data_text) + 10, font=("Arial", 10), justify="center")
        main_temp_data_entry.insert(0, main_temp_data_text)
        main_temp_data_entry.config(state="readonly")
        main_temp_data_entry.pack()
       
        temp_min_label = ttk.Label(window, text="Min Temperature:", font=("Arial", 12, "bold"), justify="center")
        temp_min_label.pack()
        temp_min_data_text = f"{data['main']['temp_min']} {temp_unit}"
        temp_min_data_entry = ttk.Entry(window, width=len(temp_min_data_text) + 10, font=("Arial", 10), justify="center")
        temp_min_data_entry.insert(0, temp_min_data_text)
        temp_min_data_entry.config(state="readonly")
        temp_min_data_entry.pack()








        temp_max_label = ttk.Label(window, text="Max Temperature:", font=("Arial", 12, "bold"), justify="center")
        temp_max_label.pack()
        temp_max_data_text = f"{data['main']['temp_max']} {temp_unit}"
        temp_max_data_entry = ttk.Entry(window, width=len(temp_max_data_text) + 10, font=("Arial", 10), justify="center")
        temp_max_data_entry.insert(0, temp_max_data_text)
        temp_max_data_entry.config(state="readonly")
        temp_max_data_entry.pack()








        feels_like_label = ttk.Label(window, text="Feels Like:", font=("Arial", 12, "bold"), justify="center")
        feels_like_label.pack()
        feels_like_data_text = f"{data['main']['feels_like']} {temp_unit}"
        feels_like_data_entry = ttk.Entry(window, width=len(feels_like_data_text) + 10, font=("Arial", 10), justify="center")
        feels_like_data_entry.insert(0, feels_like_data_text)
        feels_like_data_entry.config(state="readonly")
        feels_like_data_entry.pack()








        humidity_label = ttk.Label(window, text="Humidity:", font=("Arial", 12, "bold"), justify="center")
        humidity_label.pack()
        humidity_data_text = f"{data['main']['humidity']} %"
        humidity_data_entry = ttk.Entry(window, width=len(humidity_data_text) + 10, font=("Arial", 10), justify="center")
        humidity_data_entry.insert(0, humidity_data_text)
        humidity_data_entry.config(state="readonly")
        humidity_data_entry.pack()








        if self.temperature_unit.get() == "imperial":
            wind_speed_label = ttk.Label(window, text="Wind Speed:", font=("Arial", 12, "bold"), justify="center")
            wind_speed_label.pack()
            wind_speed_data_text = f"{data['wind']['speed']} mph"
            wind_speed_data_entry = ttk.Entry(window, width=len(wind_speed_data_text) + 10, font=("Arial", 10), justify="center")
            wind_speed_data_entry.insert(0, wind_speed_data_text)
            wind_speed_data_entry.config(state="readonly")
            wind_speed_data_entry.pack()
        else:
            wind_speed_label = ttk.Label(window, text="Wind Speed:", font=("Arial", 12, "bold"), justify="center")
            wind_speed_label.pack()
            wind_speed_data_text = f"{data['wind']['speed']} m/s"
            wind_speed_data_entry = ttk.Entry(window, width=len(wind_speed_data_text) + 10, font=("Arial", 10), justify="center")
            wind_speed_data_entry.insert(0, wind_speed_data_text)
            wind_speed_data_entry.config(state="readonly")
            wind_speed_data_entry.pack()








        visibility_label = ttk.Label(window, text="Visibility:", font=("Arial", 12, "bold"), justify="center")
        visibility_label.pack()
        visibility_data_text = f"{data['visibility']} meters"
        visibility_data_entry = ttk.Entry(window, width=len(visibility_data_text) + 10, font=("Arial", 10), justify="center")
        visibility_data_entry.insert(0, visibility_data_text)
        visibility_data_entry.config(state="readonly")
        visibility_data_entry.pack()








        # Assuming timezone_offset is the timezone offset received from the API
        timezone_offset = data['timezone']








        # Convert sunrise and sunset timestamps to datetime objects
        sunrise_timestamp = data['sys']['sunrise']
        sunset_timestamp = data['sys']['sunset']








        # Create a timezone object using the timezone offset
        timezone_name = pytz.FixedOffset(timezone_offset / 60)  # Convert seconds to minutes
        current_time = datetime.now(timezone_name)








        # Convert sunrise and sunset timestamps to datetime objects in the local timezone
        sunrise_datetime = datetime.fromtimestamp(sunrise_timestamp, timezone_name)
        sunset_datetime = datetime.fromtimestamp(sunset_timestamp, timezone_name)








        # Format sunrise and sunset times in %I:%M %p (12-hour format with AM/PM)
        sunrise_time_str = sunrise_datetime.strftime('%I:%M %p')
        sunset_time_str = sunset_datetime.strftime('%I:%M %p')








        sunrise_label = ttk.Label(window, text="Sunrise:", font=("Arial", 12, "bold"), justify="center")
        sunrise_label.pack()
        sunrise_data_text = sunrise_time_str
        sunrise_data_entry = ttk.Entry(window, width=len(sunrise_data_text) + 10, font=("Arial", 10), justify="center")
        sunrise_data_entry.insert(0, sunrise_data_text)
        sunrise_data_entry.config(state="readonly")  # Set the widget as read-only
        sunrise_data_entry.pack()








        sunset_label = ttk.Label(window, text="Sunset:", font=("Arial", 12, "bold"), justify="center")
        sunset_label.pack()
        sunset_data_text = sunset_time_str
        sunset_data_entry = ttk.Entry(window, width=len(sunset_data_text) + 10, font=("Arial", 10), justify="center")
        sunset_data_entry.insert(0, sunset_data_text)
        sunset_data_entry.config(state="readonly")  # Set the widget as read-only
        sunset_data_entry.pack()
               
    def display_5_day_forecast(self, data, city_name):
        window = tk.Toplevel()
        window.title(f"5-Day Weather Forecast in {city_name}")








        forecast_data = {}








        for forecast in data["list"]:
            forecast_date = datetime.fromtimestamp(forecast["dt"]).strftime("%Y-%m-%d")
            if forecast_date not in forecast_data:
                forecast_data[forecast_date] = forecast








        for date, data in forecast_data.items():
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            day_of_week = date_obj.strftime("%A")
            formatted_date = f"{day_of_week}, {date_obj.strftime('%B %d, %Y')}"








            forecast_label = ttk.Label(window, text=f"Date: {formatted_date}", font=("Arial", 12, "bold"))
            forecast_label.pack()








            weather_label = ttk.Label(window, text="Weather:", font=("Arial", 10, "bold"), justify="center")
            weather_label.pack()
            weather_text = data["weather"][0]["description"]
            weather_data = ttk.Entry(window, width=len(weather_text) + 10, font=("Arial", 10), justify="center")
            weather_data.insert(0, weather_text)
            weather_data.config(state="readonly")
            weather_data.pack()








            temp_unit = "°C" if self.temperature_unit.get() == "metric" else "°F"








            min_temp_text = f"{data['main']['temp_min']} {temp_unit}"
            max_temp_text = f"{data['main']['temp_max']} {temp_unit}"








            temp_min_label = ttk.Label(window, text="Min Temperature:", font=("Arial", 10, "bold"), justify="center")
            temp_min_label.pack()
            temp_min_data = ttk.Entry(window, width=len(min_temp_text) + 10, font=("Arial", 10), justify="center")
            temp_min_data.insert(0, min_temp_text)
            weather_data.config(state="readonly")
            temp_min_data.pack()








            temp_max_label = ttk.Label(window, text="Max Temperature:", font=("Arial", 10, "bold"), justify="center")
            temp_max_label.pack()
            temp_max_data = ttk.Entry(window, width=len(max_temp_text) + 10, font=("Arial", 10), justify="center")
            temp_max_data.insert(0, max_temp_text)
            weather_data.config(state="readonly")
            temp_max_data.pack()








    def popupmsg(self, title, msg):
        popup = tk.Toplevel()
        popup.title(title)
        label = ttk.Label(popup, text=msg)
        label.pack()
        B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
        B1.pack()








    def init_page(self):
        label = ttk.Label(self.window, text="Enter Location:", font=("Arial", 12, "bold"), justify="center")
        label.pack()




        location_entry = ttk.Entry(self.window, textvariable=self.location_var, font=("Arial", 12), justify="center")
        location_entry.pack()




        unit_frame = ttk.Frame(self.window)
        unit_frame.pack()




        metric_radio = ttk.Radiobutton(unit_frame, text="Metric (°C)", variable=self.temperature_unit, value="metric")
        metric_radio.grid(row=0, column=1)




        imperial_radio = ttk.Radiobutton(unit_frame, text="Imperial (°F)", variable=self.temperature_unit, value="imperial")
        imperial_radio.grid(row=0, column=2)




        current_weather_button = ttk.Button(self.window, text="Current Weather", command=self.fetch_current_weather, style="Bold.TButton")
        current_weather_button.pack()




        forecast_button = ttk.Button(self.window, text="5-Day Forecast", command=self.fetch_5_day_forecast, style="Bold.TButton")
        forecast_button.pack()


            # Button to display data visualization
        display_button = ttk.Button(self.window, text="Air Quality", command=self.display_air_quality)
        display_button.pack()


        # Entry fields for city and state
        city_label = ttk.Label(self.window, text="Enter City:", font=("Arial", 12, "bold"), justify="center")
        city_label.pack()
        city_entry = ttk.Entry(self.window, font=("Arial", 12), justify="center")
        city_entry.pack()


        state_label = ttk.Label(self.window, text="Enter State:", font=("Arial", 12, "bold"), justify="center")
        state_label.pack()
        state_entry = ttk.Entry(self.window, font=("Arial", 12), justify="center")
        state_entry.pack()


        # Button to fetch past 3 days weather data
        past_3_button = ttk.Button(self.window, text="Fetch Past 3 Days Weather", command=lambda: self.past_3(city_entry.get(), state_entry.get()))
        past_3_button.pack()




        self.window.mainloop()




if __name__ == "__main__":
    app = WeatherApp()













