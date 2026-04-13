import discord
from discord.ext import commands
from discord import app_commands
from database.message_repository import get_member_activity
import matplotlib.pyplot as plt
from matplotlib import rcParams
import io

rcParams['font.sans-serif'] = ['Microsoft JhengHei']  
rcParams['axes.unicode_minus'] = False 

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

        names = [row[1] for row in rows]  
        counts = [row[2] for row in rows]   
        
        fig, ax = plt.subplots()
        print(fig, ax)
        ax.pie(
            counts,
            textprops={'color':'w', 'weight':'bold', 'size':12},
            labels=names,
            autopct='%1.1f%%',
            startangle=140,
            labeldistance=1.1,  # 名字放到圓餅圖內
            pctdistance=0.8,      # 百分比文字位置
            # wedgeprops={'linewidth':3,'edgecolor':'w'}
        )
        ax.axis('equal')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        plt.close(fig)
        
        embed = discord.Embed(
            title=f"📈 最近 {days} 天內最活躍前 {top} 名成員",
            description="以下是統計結果：",
            color=discord.Color.blue()
        )
        
        for i, row in enumerate(rows):
            embed.add_field(
                name="",
                value=f"**{i+1}.** <@{row[0]}> 說了 **{row[2]}** 則訊息",
                inline=False
            )
        
        file = discord.File(buf, filename="activity.png")
        embed.set_image(url="attachment://activity.png")
        
        await interaction.response.send_message(file=file, embed=embed)
        
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Activity cog 已載入")

async def setup(bot):
    
    await bot.add_cog(Activity(bot))