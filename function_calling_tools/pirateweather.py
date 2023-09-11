import os
import requests
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

API_ENDPOINT = "https://api.pirateweather.net/forecast/"
PIRATE_WEATHER_API_KEY = os.environ["PIRATE_WEATHER_API_KEY"]


def fetch_weather_info(latitude, longitude):
    # https://docs.pirateweather.net/en/latest/API/
    # https://api.pirateweather.net/forecast/[apikey]/[latitude],[longitude],[time]?exclude=[excluded]&units=[unit]&extend=[hourly]&tz=[precise]
    url = f"{API_ENDPOINT}{PIRATE_WEATHER_API_KEY}/{latitude},{longitude}?exclude=minutely,hourly&units=si"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


class WeatherInput(BaseModel):
    latitude: float = Field(description="Latitude for the location to fetch the weather.")
    longitude: float = Field(description="Longitude for the location to fetch the weather.")
    # unix_timestamp: float = Field(description="current unix timestamp")


class WeatherFetcher(BaseTool):
    name = 'fetch_weather_info'
    description = "Enter latitude and longitude to get the current weather information."
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, latitude: float, longitude: float):
        return fetch_weather_info(latitude, longitude)

    def _arun(self, latitude: float, longitude: float):
        raise NotImplementedError("fetch_weather_info does not support async")
