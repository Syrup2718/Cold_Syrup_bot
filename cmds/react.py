import discord
from discord.ext import commands 
import json
import random
import requests
from bs4 import BeautifulSoup
from core.classes import Cog_Extension
import discord
from discord.ext import commands 


with open("setting.json", "r", encoding="utf-8" ) as setting:
    setting = json.load(setting)

class React(Cog_Extension):
    
    @commands.command
    async def picture(self, ctx):
        pic = discord.File()
        await ctx.send(file= pic)

async def setup(bot):
    await bot.add_cog(React(bot))