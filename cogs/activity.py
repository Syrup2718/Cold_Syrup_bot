import discord
from discord.ext import commands
from discord import app_commands
from database.message_repository import get_member_activity
import matplotlib.pyplot as plt


class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="memberactivity", description="看看誰是話癆")
    @app_commands.describe(days="幾天之內，預設為 1")
    @app_commands.describe(top="顯示前幾名，預設為 5")
    async def memberactivity(self, interaction: discord.Interaction, days: int = 1, top: int = 5):
        guild_id = str(interaction.guild.id)
        rows = get_member_activity(guild_id, days, top)
        
        if not rows:
            await interaction.response.send_message(f"最近 {days} 天沒有活動紀錄。")
            return

        result = "\n".join([f"{i+1}. <@{row[0]}>: {row[2]} 則訊息"
                            for i, row in enumerate(rows)])
        # result = "\n".join([f"{i+1}. {row[1]}: {row[2]} 則訊息"
        #                     for i, row in enumerate(rows)])
        await interaction.response.send_message(f"📈 最近 {days} 天內最活躍前 {top} 名成員：\n{result}")


    @commands.Cog.listener()
    async def on_ready(self):
        print("Activity cog 已載入")

async def setup(bot):
    
    await bot.add_cog(Activity(bot))