# ViT-Group_1

WeatherApp Documentation

Introduction
The WeatherApp is a graphical user interface (GUI) application built using Tkinter in Python. It allows users to fetch and display various weather-related data such as current weather, 5-day forecast, past 3 days weather, and air quality index (AQI) for a given location.

Dependencies
The WeatherApp requires the following Python packages to be installed:

  tkinter: Standard GUI toolkit for Python.
  requests: HTTP library for making API requests.
  PIL: Python Imaging Library for handling images.
  pytz: Library for timezone handling.
  pandas: Data manipulation and analysis library.
  matplotlib: Plotting library for creating visualizations.
  numpy: Numerical computing library.

Usage
To use the WeatherApp, simply run the script. Upon execution, a GUI window will appear where users can input the location and choose the temperature unit (metric or imperial). Then, they can click on the desired functionality buttons to fetch and display weather-related data.

Functionality

Current Weather
Fetches and displays the current weather data for the specified location, including temperature, weather condition, humidity, wind speed, visibility, sunrise, and sunset times.

5-Day Forecast
Fetches and displays the 5-day weather forecast for the specified location, including weather condition, temperature, humidity, and wind speed for each day.

Past 3 Days Weather
Fetches and displays the past 3 days weather data for the specified location, including weather condition, temperature, feels like temperature, humidity, wind speed, and wind direction.

Air Quality
Fetches and displays the air quality index (AQI) for the specified location. It visualizes the AQI using a line plot for better understanding.

Miscellaneous
Displays a quote of the day retrieved from an external API.
Provides error handling for invalid inputs and failed API requests.

Class Structure
The WeatherApp class contains methods for initializing the GUI, fetching weather data, displaying weather-related information, and handling user inputs. It is structured as follows:

  Initialization: Initializes the GUI window and sets up necessary configurations.
  Utility Methods: Includes methods for retrieving the quote of the day, sanitizing user input, fetching data from APIs, and converting wind direction.
  Display Methods: Contains methods for displaying weather-related information such as current weather, 5-day forecast, past 3 days weather, and AQI.
  Event Handling: Handles user interactions and triggers appropriate actions based on user input.
  Helper Methods: Contains helper methods for pop-up messages and initializing the GUI components.

Conclusion
The WeatherApp provides a user-friendly interface for accessing weather-related data. It leverages various APIs to fetch real-time and historical weather information, making it a valuable tool for users to plan their activities based on weather conditions.
