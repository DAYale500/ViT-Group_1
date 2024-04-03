# Here's a function to convert the wind angle from a degree to cardinal directions
# it takes in a string angle from 0-360 and returns a string


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
           return name # string is returned
   return "Unknown"  # In case the number doesn't match any range



