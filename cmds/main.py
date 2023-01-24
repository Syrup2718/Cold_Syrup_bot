import discord
from discord.ext import commands 
from core.classes import Cog_Extension

class Main(Cog_Extension):

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"現在延遲 {round(self.bot.latency * 1000)} ms") 
        print(f"現在延遲 {round(self.bot.latency * 1000)} ms")
        
def setup(bot):
    bot.add_cog(Main(bot))