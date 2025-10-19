from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import os

# Simple webserver for keep-alive checks
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()

# Discord bot setup (loads secrets from environment variables)
TOKEN = os.getenv("TOKEN")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "1410214724666134619"))
WELCOME_IMAGE_URL = os.getenv("WELCOME_IMAGE_URL", "")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        print("⚠ Welcome channel not found.")
        return

    # plain mention line
    await channel.send(f"{member.mention}")

    # embed
    embed = discord.Embed(
        title="🎉 Welcome To Eternity MC !",
        description=(
            "Welcome Player!\n"
            f"Checkout <#{WELCOME_CHANNEL_ID}>\n"
            "And Hop On Server!"
        ),
        color=0x9b59b6
    )
    if WELCOME_IMAGE_URL:
        embed.set_image(url=WELCOME_IMAGE_URL)

    await channel.send(embed=embed)

bot.run(TOKEN)