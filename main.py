import os
from dotenv import load_dotenv

load_dotenv()

from db.models import create_tables

if __name__ == "__main__":
    import sys

    create_tables()

    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        from garmin.sync import sync
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        sync(days_back=days)
    else:
        from bot.discord_bot import run
        run()
