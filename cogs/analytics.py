import discord
from discord.ext import commands
from discord import app_commands
from database.message_repository import get_top_emojis

class Analytics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="topemoji", description="看看你們最愛用什麼emoji")
    @app_commands.describe(days="幾天之內，預設為 3")
    @app_commands.describe(days="顯示前幾名，預設為 5")
    async def topemoji(self, interaction: discord.Interaction, days: int = 7, top: int = 5):
        guild_id = str(interaction.guild.id)
        results = get_top_emojis(guild_id, days, top)

        if not results:
            await interaction.response.send_message(f"最近 {days} 天沒有 emoji 使用紀錄。")
            return

        embed = discord.Embed(
            title=f"最近 {days} 天最常用的 emoji",
            description="以下是統計結果：",
            color=discord.Color.orange()
        )

        for i, (emoji, count) in enumerate(results, start=1):
            embed.add_field(
                name=f"{i}. {emoji}",
                value=f"使用次數：**{count}**",
                inline=False
            )

        await interaction.response.send_message(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print("Analytics cog 已載入")

async def setup(bot):
    await bot.add_cog(Analytics(bot))