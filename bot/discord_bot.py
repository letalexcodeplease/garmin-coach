import os
import logging

import discord
from discord.ext import commands

from coach.context_builder import build_context
from coach.llm import ask_coach
from garmin.sync import sync

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Bot connecté en tant que {bot.user}")


@bot.command(name="sync")
async def cmd_sync(ctx):
    await ctx.send("🔄 Syncing Garmin data...")
    try:
        sync(days_back=7)
        await ctx.send("✅ Data updated!")
    except Exception as e:
        logger.error(e)
        await ctx.send(f"❌ Sync error: {e}")


@bot.command(name="resume")
async def cmd_resume(ctx):
    await ctx.send("⏳ Thinking...")
    context = build_context(days=7)
    response = ask_coach("Give me a summary of my week and tell me how I'm doing overall.", context)
    await send_long(ctx, response)


@bot.command(name="fatigue")
async def cmd_fatigue(ctx):
    await ctx.send("⏳ Thinking...")
    context = build_context(days=5)
    response = ask_coach("Am I fatigued? Should I train today or rest?", context)
    await send_long(ctx, response)


@bot.command(name="nutrition")
async def cmd_nutrition(ctx):
    await ctx.send("⏳ Thinking...")
    context = build_context(days=3)
    response = ask_coach("What should I eat today based on my activity and recovery?", context)
    await send_long(ctx, response)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)
    if not message.content.startswith("/"):
        await message.channel.send("⏳ Thinking...")
        context = build_context(days=7)
        response = ask_coach(message.content, context)
        for i in range(0, len(response), 2000):
            await message.channel.send(response[i:i+2000])


async def send_long(ctx, text: str):
    for i in range(0, len(text), 2000):
        await ctx.send(text[i:i+2000])


def run():
    token = os.getenv("DISCORD_BOT_TOKEN")
    bot.run(token)
