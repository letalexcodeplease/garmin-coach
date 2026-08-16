import logging
from datetime import date, timedelta, datetime

from garmin.fetcher import get_client, fetch_activities, fetch_sleep, fetch_daily_stats
from db.models import get_session, Activity, Sleep, DailyStats

logger = logging.getLogger(__name__)

def parse_activity(raw: dict) -> dict:
    return {
        "garmin_id": str(raw.get("activityId", "")),
        "activity_type": raw.get("activityType", {}).get("typeKey"),
        "name": raw.get("activityName"),
        "start_time": datetime.fromisoformat(raw["startTimeLocal"]) if raw.get("startTimeLocal") else None,
        "duration_seconds": raw.get("duration"),
        "distance_meters": raw.get("distance"),
        "avg_hr": raw.get("averageHR"),
        "max_hr": raw.get("maxHR"),
        "calories": raw.get("calories"),
        "avg_pace": raw.get("averageSpeed"),
        "elevation_gain": raw.get("elevationGain"),
        "aerobic_te": raw.get("aerobicTrainingEffect"),
        "raw": raw,
    }

def parse_sleep(raw: dict, target_date: date) -> dict | None:
    daily = raw.get("dailySleepDTO", {})
    if not daily:
        return None
    return {
        "date": target_date,
        "duration_seconds": daily.get("sleepTimeSeconds"),
        "deep_sleep_seconds": daily.get("deepSleepSeconds"),
        "light_sleep_seconds": daily.get("lightSleepSeconds"),
        "rem_sleep_seconds": daily.get("remSleepSeconds"),
        "awake_seconds": daily.get("awakeSleepSeconds"),
        "avg_spo2": daily.get("averageSpO2Value"),
        "avg_stress": daily.get("avgSleepStress"),
        "sleep_score": daily.get("sleepScores", {}).get("overall", {}).get("value"),
        "raw": raw,
    }

def parse_daily(raw: dict, target_date: date) -> dict:
    return {
        "date": target_date,
        "steps": raw.get("totalSteps"),
        "calories_total": raw.get("totalKilocalories"),
        "calories_active": raw.get("activeKilocalories"),
        "avg_stress": raw.get("averageStressLevel"),
        "max_stress": raw.get("maxStressLevel"),
        "resting_hr": raw.get("restingHeartRate"),
        "hrv_status": raw.get("hrvStatus"),
        "body_battery_high": raw.get("bodyBatteryHighestValue"),
        "body_battery_low": raw.get("bodyBatteryLowestValue"),
        "raw": raw,
    }

def sync(days_back: int = 7):
    logger.info(f"Garmin sync — last {days_back} days")
    client = get_client()
    session = get_session()
    today = date.today()
    start = today - timedelta(days=days_back)

    activities = fetch_activities(client, start, today)
    for raw in activities:
        data = parse_activity(raw)
        existing = session.query(Activity).filter_by(garmin_id=data["garmin_id"]).first()
        if not existing:
            session.add(Activity(**data))
    session.commit()
    logger.info(f"{len(activities)} activities processed")

    for n in range(days_back + 1):
        target = start + timedelta(days=n)

        sleep_raw = fetch_sleep(client, target)
        if sleep_raw:
            parsed = parse_sleep(sleep_raw, target)
            if parsed:
                existing = session.query(Sleep).filter_by(date=target).first()
                if existing:
                    for k, v in parsed.items():
                        setattr(existing, k, v)
                else:
                    session.add(Sleep(**parsed))

        daily_raw = fetch_daily_stats(client, target)
        if daily_raw:
            parsed = parse_daily(daily_raw, target)
            existing = session.query(DailyStats).filter_by(date=target).first()
            if existing:
                for k, v in parsed.items():
                    setattr(existing, k, v)
            else:
                session.add(DailyStats(**parsed))

        session.commit()

    logger.info("Sync complete")
