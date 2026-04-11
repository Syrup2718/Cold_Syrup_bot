import discord
from discord.ext import commands
from discord import app_commands


class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="meow", description="喵一下")
    @app_commands.describe(num="多喵幾下，預設為 1")
    async def meow(self, interaction: discord.Interaction, num: int = 1):
        await interaction.response.send_message("喵" * num)


    @commands.Cog.listener()
    async def on_ready(self):
        print("Trivia cog 已載入")

async def setup(bot):
    await bot.add_cog(Trivia(bot))