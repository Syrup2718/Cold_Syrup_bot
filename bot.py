import discord
from discord.ext import commands 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='[', intents=intents)

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    print(f"{member} join!")

@bot.event
async def on_member_remove(member):
    print(f"{member} leave!")

bot.run("MTA2NDc3MzQ3MzEyNzM2NjcwNw.GxSyaM.pPbcJuGmkL0heWJm_qa0RoZ4R4gYH1jK4VzcuA")