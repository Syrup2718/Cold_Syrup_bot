import discord
from discord.ext import commands 
import json
from core.classes import Cog_Extension
import random

with open("setting.json", "r", encoding="utf-8" ) as setting:
    setting = json.load(setting)

class Event(Cog_Extension):

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} join!")
        channel = self.bot.get_channel(setting["Welcome_channel"])
        await channel.send(f"{member} join!")
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} leave!")
        channel = self.bot.get_channel(setting["Leave_channel"])
        await channel.send(f"{member} leave!")

    

    @commands.Cog.listener()
    async def on_message(self, msg):
        say_hi = ["早安", "安", "午安", "晚安", "安安", "hi", "Hi", "HI", "Hello", "hello"]
        if len(list(filter(lambda str:msg.content.endswith(str), say_hi))) and msg.author.id != 1064773473127366707:
            await msg.channel.send(random.choice(say_hi))

        


async def setup(bot):
    await bot.add_cog(Event(bot))


