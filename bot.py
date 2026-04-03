import discord
from discord.ext import commands
import json

with open("setting.json", "r") as f:
    token = json.load(f)["TOKEN"]

print(token)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print("\n")
    print(".. 𖥧 𖥧 𖧧 ˒˒. . 𖡼.𖤣𖥧 ⠜ . . 𖥧 𖥧 𖧧 ˒˒. . 𖡼.𖤣𖥧 ⠜. . 𖥧 𖥧 𖧧 ˒˒..")
    print(f"該吃藥啦 不然我要來把你們抓走惹")
    print(f"{client.user} 起床了喔 (ID: {client.user.id})")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    
    if message.content == "gay":
        await message.channel.send("You are GAY!")




