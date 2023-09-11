import ntplib
import pytz
from datetime import datetime, timezone
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool


def fetch_current_datetime_in_timezone(timezone_str):
    client = ntplib.NTPClient()
    response = client.request('pool.ntp.org')
    utc_now = datetime.fromtimestamp(response.tx_time, timezone.utc)
    try:
        target_timezone = pytz.timezone(timezone_str)
        return utc_now.astimezone(target_timezone)
    except pytz.UnknownTimeZoneError:
        raise ValueError(f"Unsupported timezone: {timezone_str}")


class TimeZoneDatetimeInput(BaseModel):
    timezone_str: str = Field(description="Time zone (e.g., Asia/Tokyo, UTC, America/New_York, Europe/London, etc.)")


class TimeZoneDatetimeFetcher(BaseTool):
    name = 'fetch_datetime_in_timezone'
    description = "Enter time zone (e.g., Asia/Tokyo, UTC, America/New_York, Europe/London, etc.). Outputs the current date and time corresponding to the time zone."
    args_schema: Type[BaseModel] = TimeZoneDatetimeInput

    def _run(self, timezone_str: str):
        return fetch_current_datetime_in_timezone(timezone_str)

    def _arun(self, ticker: str):
        raise NotImplementedError("fetch_datetime_in_timezone does not support async")
