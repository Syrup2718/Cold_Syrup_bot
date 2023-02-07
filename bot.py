import discord
from discord.ext import commands 
import json
import random
import requests
from bs4 import BeautifulSoup
import os   

with open("setting.json", "r", encoding="utf-8" ) as setting:
    setting = json.load(setting)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    for filename in os.listdir('./cmds'):
        if filename.endswith(".py"):
            await bot.load_extension(f"cmds.{filename[:-3]}")
            print(f"cmds.{filename[:-3]}")
    print(">> Bot is online <<")


if __name__ == "__main__":
    bot.run(setting["TOKEN"])    
