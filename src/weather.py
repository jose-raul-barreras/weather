"""
Weather class to retrieve and parse weather data from the National Weather Service (NWS) API
"""

import xml.etree.ElementTree as ET
import requests

LOCATIONS = {"KLNK": "Lincoln", "KOMA": "Omaha"}


class Weather:
    """
    Weather class to retrieve and parse weather data from the National Weather Service (NWS) API
    """

    def __init__(self, observation_location=None):
        if observation_location:
            self.set_location(observation_location)
        else:
            self._location = None
            self.weather_observation_url = None
            self.weather_observation_raw = None

    def read_weather_observation(self, url):
        """Read weather observation data from the URL"""
        try:
            # Send a GET request to the URL
            response = requests.get(url, timeout=1000)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Read the content from the response
                weather_observation = response.text
                return weather_observation
            else:
                print("Failed to retrieve data. Status code:", response.status_code)
                return None

        except requests.exceptions.RequestException as exp:
            print("An error occurred:", str(exp))
            return None

    def set_location(self, observation_location):
        """Set the observation location and update the weather observation URL"""
        self._location = observation_location
        self.weather_observation_url = (
            f"https://w1.weather.gov/xml/current_obs/{self._location}.xml"
        )
        self.weather_observation_raw = self.read_weather_observation(
            self.weather_observation_url
        )
        self.root = ET.fromstring(self.weather_observation_raw)

    def get_location(self):
        """Return the location"""
        return self.root.find("location").text

    location = property(get_location, set_location)

    @property
    def temperature(self) -> str:
        """Return the temperature in degrees Fahrenheit and Celsius"""
        temp_f = float(self.root.find("temp_f").text)
        temp_c = float(self.root.find("temp_c").text)
        return f"{temp_f}°F ({temp_c}°C)"

    @property
    def relative_humidity(self) -> str:
        """Return the relative humidity as a percentage"""
        relative_humidity = self.root.find("relative_humidity")
        return relative_humidity.text + "%"

    @property
    def weather(self) -> str:
        """Return the weather description"""
        return self.root.find("weather").text

    @property
    def wind_info(self) -> str:
        """Return the wind information"""
        wind_string = self.root.find("wind_string").text
        return wind_string

    @property
    def dewpoint(self) -> str:
        """Return the dewpoint in degrees Fahrenheit and Celsius"""
        dewpoint_c = float(self.root.find("dewpoint_c").text)
        dewpoint_f = float(self.root.find("dewpoint_f").text)
        return f"{dewpoint_c}°C ({dewpoint_f}°F)"

    @property
    def pressure(self) -> str:
        """Return the pressure in millibars and inches of mercury"""
        pressure_mb = float(self.root.find("pressure_mb").text)
        return f"{pressure_mb} mb"

    @property
    def altimeter(self) -> str:
        """Return the altimeter in inches of mercury"""
        altimeter_in = float(self.root.find("pressure_in").text)
        return f"{altimeter_in} in Hg"

    @property
    def visibility(self) -> str:
        """Return the visibility in miles and kilometers"""
        visibility_mi = float(self.root.find("visibility_mi").text)
        visibility_km = visibility_mi * 1.609344
        return f"{visibility_mi} mi ({visibility_km} km)"

    def __str__(self) -> str:
        """Return a string representation of the object"""
        return f"""
        Location: {self.location}
        Weather: {self.weather}
        Temperature: {self.temperature}
        Dewpoint: {self.dewpoint}
        Relative Humidity: {self.relative_humidity}
        Wind: {self.wind_info}
        Visibility: {self.visibility}
        Pressure: {self.pressure}
        Altimeter: {self.altimeter}
        """


# Use CLI to run the program. If the file is imported, the code below will not run.
# The code below is only executed if the file is run directly.
# This allows us to import the Weather class into other files without running the code below.
# This is useful for testing the Weather class.
# The program can be run from the command line with the following command:
# python weather.py --location KLNK

if __name__ == "__main__":
    import click

    @click.command()
    @click.option("--location", help="Specify a location")
    @click.option("--list-locations", is_flag=True, help="List all locations")
    def main(location, list_locations):
        """Main function"""
        if not location and not list_locations:
            # No options provided, print the help message
            click.echo(click.get_current_context().get_help())
        if location:
            click.echo(f"Location specified: {location}")
            current_weather = Weather(observation_location=location)
            print(current_weather)
        elif list_locations:
            click.echo("Possible locations:")
            for location, value in LOCATIONS.items():
                click.echo(location + " - " + value)
        else:
            click.echo("No location specified. Use --location to specify a location.")

    main(None, None)
