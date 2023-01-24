import discord
from discord.ext import commands 


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    print(f"{member} join!")
    channel = bot.get_channel(886002454238486588)
    await channel.send(f"{member} join!")

@bot.event
async def on_member_remove(member):
    print(f"{member} leave!")
    channel = bot.get_channel(886006875982798848)
    await channel.send(f"{member} leave!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"現在延遲 {round(bot.latency * 1000)} ms") 


bot.run("MTA2NDc3MzQ3MzEyNzM2NjcwNw.GAMZuz.UVV0xEy5G16a3023lKr5I-607rXUNdxDvez2tU")  