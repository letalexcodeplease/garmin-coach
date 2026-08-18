import os
import logging
from datetime import date

from garminconnect import Garmin

logger = logging.getLogger(__name__)


def get_client() -> Garmin:
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    client = Garmin(email, password)
    client.login()
    return client


def fetch_activities(client: Garmin, start: date, end: date) -> list[dict]:
    try:
        return client.get_activities_by_date(start.isoformat(), end.isoformat()) or []
    except Exception as e:
        logger.error(f"fetch activities error: {e}")
        return []


def fetch_sleep(client: Garmin, target_date: date) -> dict | None:
    try:
        return client.get_sleep_data(target_date.isoformat())
    except Exception as e:
        logger.error(f"fetch sleep error {target_date}: {e}")
        return None


def fetch_daily_stats(client: Garmin, target_date: date) -> dict | None:
    try:
        return client.get_user_summary(target_date.isoformat())
    except Exception as e:
        logger.error(f"fetch daily stats error {target_date}: {e}")
        return None
