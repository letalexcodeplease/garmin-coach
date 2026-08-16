from datetime import date, timedelta

from db.models import get_session, Activity, Sleep, DailyStats

def build_context(days: int = 7) -> str:
    session = get_session()
    today = date.today()
    start = today - timedelta(days=days)

    activities = (
        session.query(Activity)
        .filter(Activity.start_time >= start)
        .order_by(Activity.start_time.desc())
        .all()
    )

    sleeps = (
        session.query(Sleep)
        .filter(Sleep.date >= start)
        .order_by(Sleep.date.desc())
        .all()
    )

    daily = (
        session.query(DailyStats)
        .filter(DailyStats.date >= start)
        .order_by(DailyStats.date.desc())
        .all()
    )

    lines = [f"Garmin data — last {days} days (today: {today})\n"]

    if activities:
        lines.append("## Recent activities")
        for a in activities[:10]:
            dist = f"{a.distance_meters/1000:.1f}km" if a.distance_meters else "N/A"
            dur = f"{int(a.duration_seconds//60)}min" if a.duration_seconds else "N/A"
            hr = f"avg HR {a.avg_hr:.0f}bpm" if a.avg_hr else ""
            te = f"TE {a.aerobic_te:.1f}" if a.aerobic_te else ""
            lines.append(f"- {a.start_time.strftime('%d/%m') if a.start_time else '?'} {a.activity_type or a.name}: {dist}, {dur}, {hr}, {te}")

    if sleeps:
        lines.append("\n## Recent sleep")
        for s in sleeps[:7]:
            total = s.duration_seconds / 3600 if s.duration_seconds else 0
            score = f"score {s.sleep_score:.0f}" if s.sleep_score else ""
            deep = f"deep {s.deep_sleep_seconds/3600:.1f}h" if s.deep_sleep_seconds else ""
            lines.append(f"- {s.date}: {total:.1f}h {score} {deep}")

    if daily:
        lines.append("\n## Recent daily stats")
        for d in daily[:7]:
            bb = f"Body Battery {d.body_battery_high:.0f}↑/{d.body_battery_low:.0f}↓" if d.body_battery_high else ""
            stress = f"avg stress {d.avg_stress:.0f}" if d.avg_stress else ""
            rhr = f"resting HR {d.resting_hr:.0f}bpm" if d.resting_hr else ""
            lines.append(f"- {d.date}: {bb} {stress} {rhr}")

    return "\n".join(lines)
