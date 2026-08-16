# 🏃 Garmin Coach

Personal Discord bot that fetches Garmin Connect data and acts as your sports and nutrition coach via Gemini 2.0 Flash.

## 🛠 Stack

- **Python 3.11+**
- **PostgreSQL** — stores Garmin data (activities, sleep, daily stats)
- **SQLAlchemy** — ORM, no raw SQL queries
- **garminconnect** — unofficial lib for the Garmin Connect API
- **discord.py** — bot interface
- **google-generativeai** — Gemini 2.0 Flash

## 📁 Structure

```
main.py                  # Entry point: starts the bot or runs a sync
db/models.py             # SQLAlchemy models (Activity, Sleep, DailyStats)
garmin/fetcher.py        # Garmin Connect client with session cache
garmin/sync.py           # Syncs Garmin data → PostgreSQL
coach/context_builder.py # Builds text context from the database
coach/llm.py             # Gemini call with coach system prompt
bot/discord_bot.py       # Discord handlers (/sync /resume /fatigue /nutrition)
```

## 🚀 Installation

```bash
# Create a .env file and fill in your credentials (see Environment variables below)

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Initial sync (last 7 days)
python main.py sync

# Start the bot
python main.py
```

## 🔑 Environment variables (.env)

| Variable | Description |
|----------|-------------|
| `GARMIN_EMAIL` | Your Garmin Connect email |
| `GARMIN_PASSWORD` | Your Garmin Connect password |
| `DATABASE_URL` | e.g. `postgresql://user:password@localhost:5432/garmin_coach` |
| `DISCORD_BOT_TOKEN` | From the [Discord Developer Portal](https://discord.com/developers/applications) |
| `GEMINI_API_KEY` | From [aistudio.google.com](https://aistudio.google.com) |

## 🤖 Discord commands

| Command | Description |
|---------|-------------|
| `/sync` | Sync latest Garmin data |
| `/resume` | Weekly summary |
| `/fatigue` | Am I fatigued? Should I train today? |
| `/nutrition` | Nutrition advice for the day |

You can also send any free-text message and the coach will answer based on your data.

## ⚙️ Conventions

- Garmin parsing logic lives in `garmin/sync.py`
- The context sent to the LLM is built in `coach/context_builder.py`
- No raw SQL — always go through SQLAlchemy
- Raw Garmin data is stored in the `raw` JSON column for re-parsing without re-fetching
- The Garmin session is cached in `garmin_session.json` (gitignored) to avoid re-logging in every time
