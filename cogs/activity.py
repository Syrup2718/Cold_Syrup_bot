import discord
from discord.ext import commands
from discord import app_commands

class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="memberactivity", description="看看誰是話癆")
    @app_commands.describe(days="幾天之內，預設為 1")
    @app_commands.describe(top="顯示前幾名，預設為 5")
    async def memberactivity(self, interaction: discord.Interaction, days: int = 1, top: int = 5):
        print(interaction.guild.id)


    @commands.Cog.listener()
    async def on_ready(self):
        print("Activity cog 已載入")

async def setup(bot):
    
    await bot.add_cog(Activity(bot))