import discord
from discord.ext import commands
import json
import os
import asyncio
from database.db import init_db

init_db()

ID = 1461387152326787094

with open("setting.json", "r") as f:
    token = json.load(f)["TOKEN"]   
    
print(token)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print("\n")
    print(".. 𖥧 𖥧 𖧧 ˒˒. . 𖡼.𖤣𖥧 ⠜ . . 𖥧 𖥧 𖧧 ˒˒. . 𖡼.𖤣𖥧 ⠜. . 𖥧 𖥧 𖧧 ˒˒..")
    print(f"該吃藥啦 不然我要來把你們抓走惹")
    print(f"{bot.user} 起床了喔 (ID: {bot.user.id})")

    print(".. 𖥧 𖥧 𖧧 ˒˒. . 𖡼.𖤣𖥧 ⠜ . . 𖥧 𖥧 𖧧 ˒˒. . 𖡼.𖤣𖥧 ⠜. . 𖥧 𖥧 𖧧 ˒˒..")
    slash = await bot.tree.sync()
    print(f"總共載入 {len(slash)} 個指令")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="把泥抓去賣掉！！！"))



async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(token=token)

if __name__ == "__main__":
    asyncio.run(main())
