import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
import requests
from datetime import datetime
from datetime import datetime, timedelta
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL library
import pytz  # Import pytz for timezone handling
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
api_key = "29b6f476ddbbec25a80a7d86634f3399"

api_key_visualcrossing = "9LMZ7SVJRRQN9QQ4XCHK46VBN"

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

class WeatherApp:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Weather App")
        self.window.geometry("600x400")
        self.window.configure(bg='white')

        self.location_var = tk.StringVar()
        self.temperature_unit = tk.StringVar(value="metric")
       
        self.quote_of_the_day = self.get_quote_of_the_day()

        # Configure ttk Style for dark blue theme
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as a base
        self.style.configure('.', foreground='black', background='light blue')  # Set foreground and background colors for all widgets
        self.style.map('.', foreground=[('disabled', 'gray')])  # Set disabled widget color to gray

        # Customize specific widget elements for dark blue theme
        self.style.configure('TButton', foreground='black', background='light blue', font=('Arial', 14, 'bold'))
        self.style.map('TButton', foreground=[('active', 'orange')])  # Set active button color to orange
        self.style.configure('TLabel', foreground='black', background='light blue', font=('Arial', 14, 'bold'))
        self.style.configure('TEntry', foreground='black', background='light blue', font=('Arial', 14))
        self.style.configure('TRadiobutton', foreground='black', background='light blue', font=('Arial', 14))

        # Display the quote of the day and international holiday in the GUI
        self.display_quote()

        # Dictionary containing weather icons represented as text
        self.weather_icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Snow": "❄️",
            "Thunderstorm": "⛈️",
            "Mist": "🌫️",
            "Haze": "🌫️",
            "Fog": "🌫️",
            "Smoke": "🌫️",
            "Drizzle": "🌦️",
            "Sleet": "🌨️",
            "Tornado": "🌪️",
            "Sunny": "🌞",
            "Partly Cloudy": "⛅",
            "Mostly Cloudy": "🌥️",
            "Overcast": "🌥️"
        }

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
        quote_label = ttk.Label(self.window, text="🙏🧘A Quote to Live By🧘🙏", font=("Arial", 14, "bold"), justify="center")
        quote_label.pack()
        quote_entry = ttk.Entry(self.window, width=len(self.quote_of_the_day), font=("Arial", 12), justify="center")
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
         # Replace spaces with "%20" in the city name
        city = city.replace(" ", "%20")

        base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        complete_url = f"{base_url}{city}/last3days?unitGroup=us&key={api_key_visualcrossing}"
        print(complete_url)

        data = self.get_data(complete_url)
        print(data)
        
        if data:
            print("Past 3 days weather data:", data)

            window = tk.Toplevel()
            window.title(f"Past 3 Days Weather in {data['resolvedAddress']}")

            print(data["days"])

            advisory_label = ttk.Label(window, text="Note: Check window title. If it is not the correct location, please specify your search further.", font=("Arial", 10))
            advisory_label.pack()

            for day_data in data["days"][1:]:
                date_label = ttk.Label(window, text=f"Date: {datetime.fromtimestamp(day_data['datetimeEpoch']).strftime('%B %d, %Y')}", font=("Arial", 12, "bold"))
                date_label.pack()

                weather_label = ttk.Label(window, text=f"Weather: {day_data['conditions']}", font=("Arial", 10))
                weather_label.pack()

                temp_label = ttk.Label(window, text=f"Temperature: {day_data['temp']}°F", font=("Arial", 10))
                temp_label.pack()

                feels_like_label = ttk.Label(window, text=f"Feels Like: {day_data['feelslike']}°F", font=("Arial", 10))
                feels_like_label.pack()

                humidity_label = ttk.Label(window, text=f"Humidity: {day_data['humidity']}%", font=("Arial", 10))
                humidity_label.pack()

                wind_speed_label = ttk.Label(window, text=f"Wind Speed: {day_data['windspeed']} mph", font=("Arial", 10))
                wind_speed_label.pack()

                wind_direction_label = ttk.Label(window, text=f"Wind Direction: {self.get_cardinal_direction(day_data['winddir'])}", font=("Arial", 10))
                wind_direction_label.pack()

                separator = ttk.Separator(window, orient="horizontal")
                separator.pack(fill="x", padx=10, pady=5)

        else:
            self.popupmsg("Error", "Failed to fetch data from API.")

    def create_air_quality(self, city_name):
        # Get data from API using the WeatherApp's get_data method
        api_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}?unitGroup=metric&key=9LMZ7SVJRRQN9QQ4XCHK46VBN&contentType=json&elements=datetime,pm1,pm2p5,pm10,o3,no2,so2,co,aqius,aqieur"
        data = self.get_data(api_url)
        print(data)

        if data:
            df = pd.DataFrame(data["days"])

            # Define AQI ranges and corresponding colors
            aqi_ranges = [(0, 50), (51, 100), (101, 150), (151, 200), (201, 300), (301, float('inf'))]
            aqi_colors = ['green', 'yellow', 'orange', 'red', 'purple', 'maroon']
            aqi_labels = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']

            # Create a new window for the plot
            plot_window = tk.Toplevel(self.window)
            plot_window.title(f"Air Quality Index (AQI) in {data['resolvedAddress']}")
            plot_window.geometry("800x600")

            # Create a Matplotlib figure
            fig, ax = plt.subplots(figsize=(8, 6))

            # Iterate over AQI ranges and plot corresponding background colors
            for i, (start, end) in enumerate(aqi_ranges):
                ax.axhspan(start, end, color=aqi_colors[i], alpha=0.3, label=aqi_labels[i])

            # Plot AQI data
            ax.plot(df["datetime"], df["aqius"], label="AQI (US)", linewidth=6)

            # Set labels and title
            ax.set_xlabel("Date")
            ax.set_ylabel("AQI")
            ax.set_title(f"Air Quality Index (AQI) in {data['resolvedAddress']}")
            ax.legend()
            ax.grid(True)
            fig.tight_layout()

            # Define hover functionality to display descriptions
            def hover(event):
                for i, (start, end) in enumerate(aqi_ranges):
                    if start <= event.ydata <= end:
                        text = f'{aqi_labels[i]}: {start} to {end}'
                        tooltip = ax.text(event.xdata, event.ydata, text, bbox=dict(facecolor=aqi_colors[i], alpha=0.5))

            fig.canvas.mpl_connect('motion_notify_event', hover)

            # Embed the Matplotlib plot into Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.get_tk_widget().pack()

            # Display the plot
            canvas.draw()

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
                print(current_weather_data)
                if current_weather_data:
                    self.display_current_weather(current_weather_data, city_name)
                else:
                    self.popupmsg("Error", "Weather data not available.")
            else:
                self.popupmsg("Error", 'Geocode data not available/invalid input. Check spelling. Input structure must follow "City","State" (optional), "Country".')
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
                print(forecast_data)
                if forecast_data:
                    self.display_5_day_forecast(forecast_data, city_name)
                else:
                    self.popupmsg("Error", "Forecast data not available.")
            else:
                self.popupmsg("Error", 'Geocode data not available/invalid input. Check spelling. Input structure must follow "City","State" (optional), "Country".')
        else:
            self.popupmsg("Error", "Invalid input format.")
    
    def get_cardinal_direction(self, degrees):
        cardinal_directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        idx = round(degrees / 45) % 8
        return cardinal_directions[idx]

    def display_past_3(self):
        input_location = self.location_var.get()
        if not input_location:
            self.popupmsg("Error", "Please enter a valid location.")
            return

        city, state = self.sanitize_user_input(input_location)
        if not city or not state:
            self.popupmsg("Error", "Invalid input format. Please provide a city and state.")
            return

        self.past_3(city, state)

    def display_current_weather(self, data, city_name):
        window = tk.Toplevel()
        window.title(f"Current Weather in {city_name}, {data['sys']['country']}")

        advisory_label = ttk.Label(window, text="Note: Check window title. If it is not the correct location, please specify your search further.", font=("Arial", 10))
        advisory_label.pack()

        weather_condition = data["weather"][0]["main"]  # Ensure lowercase for matching

        # Get weather icon text
        weather_icon_text = self.weather_icons.get(weather_condition, self.weather_icons[weather_condition])

        # Display weather icon as label
        weather_icon_label = ttk.Label(window, text=weather_icon_text, font=("Arial", 40))
        weather_icon_label.pack()
       
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
            wind_speed_label = ttk.Label(window, text="Wind Speed & Direction:", font=("Arial", 12, "bold"), justify="center")
            wind_speed_label.pack()
            wind_speed_data_text = f"{data['wind']['speed']} mph {self.get_cardinal_direction(data['wind']['speed'])}"
            wind_speed_data_entry = ttk.Entry(window, width=len(wind_speed_data_text) + 10, font=("Arial", 10), justify="center")
            wind_speed_data_entry.insert(0, wind_speed_data_text)
            wind_speed_data_entry.config(state="readonly")
            wind_speed_data_entry.pack()
        else:
            wind_speed_label = ttk.Label(window, text="Wind Speed & Direction:", font=("Arial", 12, "bold"), justify="center")
            wind_speed_label.pack()
            wind_speed_data_text = f"{data['wind']['speed']} m/s {self.get_cardinal_direction(data['wind']['speed'])}"
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
        window.title(f"5-Day Weather Forecast in {city_name}, {data['city']['country']}")
    
        forecast_data = {}

        advisory_label = ttk.Label(window, text="Note: Check window title. If it is not the correct location, please specify your search further.", font=("Arial", 10))
        advisory_label.pack()
    
        for forecast in data["list"][1:]:
            forecast_date = datetime.fromtimestamp(forecast["dt"]).strftime("%Y-%m-%d")
            if forecast_date not in forecast_data:
                forecast_data[forecast_date] = forecast
    
        for date, data in forecast_data.items():
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            day_of_week = date_obj.strftime("%A")
            formatted_date = f"{day_of_week}, {date_obj.strftime('%B %d, %Y')}"
    
            forecast_label = ttk.Label(window, text=f"Date: {formatted_date}", font=("Arial", 12, "bold"))
            forecast_label.pack()
    
            weather_label = ttk.Label(window, text="Weather:", font=("Arial", 10, "bold"))
            weather_label.pack()
            weather_text = data["weather"][0]["description"]
            weather_data = ttk.Entry(window, width=30, font=("Arial", 10), justify="center")
            weather_data.insert(0, weather_text)
            weather_data.config(state="readonly")
            weather_data.pack()
    
            temp_unit = "°C" if self.temperature_unit.get() == "metric" else "°F"
            temp_text = f"Temperature: {data['main']['temp']} {temp_unit}"
            humidity_text = f"Humidity: {data['main']['humidity']} %"
    
            if self.temperature_unit.get() == "imperial":
                wind_speed_unit = "mph"
                wind_speed = f"Wind Speed & Direction: {data['wind']['speed']} {wind_speed_unit}"
            else:
                wind_speed_unit = "m/s"
                wind_speed = f"Wind Speed & Direction: {data['wind']['speed']} {wind_speed_unit}"
    
            wind_deg = data['wind']['deg']
            wind_dir_text = self.get_cardinal_direction(wind_deg)
    
            temp_data = ttk.Label(window, text=temp_text, font=("Arial", 10))
            temp_data.pack()
            humidity_data = ttk.Label(window, text=humidity_text, font=("Arial", 10))
            humidity_data.pack()
            wind_speed_data = ttk.Label(window, text=f'{wind_speed} {wind_dir_text}', font=("Arial", 10))
            wind_speed_data.pack()

    def popupmsg(self, title, msg):
        popup = tk.Toplevel()
        popup.title(title)
        label = ttk.Label(popup, text=msg)
        label.pack()
        B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
        B1.pack()

    def init_page(self):
        label = ttk.Label(self.window, text="🗺️Enter Location:🗺️", font=("Arial", 14, "bold"), justify="center")
        label.pack()

        location_entry = ttk.Entry(self.window, textvariable=self.location_var, font=("Arial", 14), justify="center")
        location_entry.pack()

        unit_frame = ttk.Frame(self.window)
        unit_frame.pack()

        metric_radio = ttk.Radiobutton(unit_frame, text="Metric (°C)", variable=self.temperature_unit, value="metric")
        metric_radio.grid(row=0, column=1)

        imperial_radio = ttk.Radiobutton(unit_frame, text="Imperial (°F)", variable=self.temperature_unit, value="imperial")
        imperial_radio.grid(row=0, column=2)

        current_weather_button = ttk.Button(self.window, text="🚨Current Weather🚨", command=self.fetch_current_weather, style="Bold.TButton")
        current_weather_button.pack()

        forecast_button = ttk.Button(self.window, text="📅5-Day Forecast📅", command=self.fetch_5_day_forecast, style="Bold.TButton")
        forecast_button.pack()

        # Button to display data visualization
        display_button = ttk.Button(self.window, text="😷Air Quality😷", command=self.display_air_quality)
        display_button.pack()

        # Button to fetch past 3 days weather data
        past_3_button = ttk.Button(self.window, text="🔄Past 3 Days Weather🔄", command=self.display_past_3, style="Bold.TButton")
        past_3_button.pack()

        self.window.mainloop()

if __name__ == "__main__":
    app = WeatherApp()
