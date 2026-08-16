# Garmin Coach — CLAUDE.md

## Goal
Personal Discord bot that fetches Garmin Connect data and provides sports/nutrition coaching via Gemini 2.0 Flash. Data is stored in PostgreSQL.

## Stack
- Python 3.11+
- PostgreSQL + SQLAlchemy (ORM)
- garminconnect (unofficial Garmin API)
- discord.py (bot interface)
- google-generativeai (Gemini 2.0 Flash)
- python-dotenv

## Project structure
```
main.py                  # Entry point: bot or sync mode
db/models.py             # SQLAlchemy models + singleton engine/session
garmin/fetcher.py        # Garmin Connect client with session cache
garmin/sync.py           # Syncs Garmin data → PostgreSQL
coach/context_builder.py # Builds LLM context from DB
coach/llm.py             # Gemini call with system prompt
bot/discord_bot.py       # Discord bot handlers
```

## Discord commands
- `/sync` — sync Garmin data (last 7 days)
- `/resume` — weekly summary
- `/fatigue` — fatigue assessment
- `/nutrition` — nutrition advice
- Free text → coach answers based on Garmin data

## Architecture notes
- `get_engine()` and `get_session()` use a singleton pattern — engine is created once
- Garmin session cached in `garmin_session.json` (gitignored) to avoid repeated logins
- Raw Garmin JSON stored in `raw` column on each model — allows re-parsing without re-fetching
- LLM context built from DB in `context_builder.py` — this controls what the coach "sees"

## Conventions
- No raw SQL — always use SQLAlchemy
- snake_case everywhere
- No comments unless logic is non-obvious

## Environment variables
See `.env.example` for all required variables. Never commit `.env`.

## Useful commands
- `python main.py sync [N]` — sync last N days (default 7)
- `python main.py` — start the Discord bot

## Do not
- Add raw SQL queries
- Commit `.env` or `garmin_session.json`
