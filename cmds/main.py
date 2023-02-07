import discord
from discord.ext import commands 
from core.classes import Cog_Extension
import json
import random

class Main(Cog_Extension):

    #新增embed
    @commands.command() 
    async def em(self, ctx):
        print(f"{ctx.author} use !em")
        embed=discord.Embed(title="關於", description="就你自己啊:/", color=0x0693fe)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=ctx.author.avatar)
        embed.add_field(name="User ID: ", value=ctx.author.id, inline=True)
        embed.set_footer(text="持續更新中:P")
        await ctx.send(embed=embed)

    #查詢ping
    @commands.command()
    async def ping(self, ctx):
        print(f"{ctx.author} use !ping")
        await ctx.send(f"現在延遲 {round(self.bot.latency * 1000)} ms") 
        print(f"現在延遲 {round(self.bot.latency * 1000)} ms")
    
    #BOT複誦
    @commands.command()
    async def sayd(self, ctx, *,msg):
        print(f"{ctx.author} use !sayd and say {msg}")
        await ctx.message.delete()
        await ctx.send(msg)

    #清理訊息
    @commands.command()
    async def purge(self, ctx, num: int):
        print(f"{ctx.author} use !sayd and purge {num}")
        await ctx.channel.purge(limit=num+1)

    #不妙的隨機
    @commands.command()
    async def nw(self, ctx):
        print(f"{ctx.author} use !nw")
        num = random.randint(1, 440000)
        print(f"||~~https://nhentai.net/g/{num}/ ~~|| 可能是404就是了.w. 不過會在完善的awa")
        await ctx.send(f"||~~https://nhentai.net/g/{num}/ ~~|| 可能是404就是了.w. 不過會在完善的awa")
        
        




    
        
async def setup(bot):
    await bot.add_cog(Main(bot))