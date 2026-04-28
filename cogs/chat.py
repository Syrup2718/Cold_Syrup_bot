import discord
from discord.ext import commands
from discord import app_commands
from services import chat_model

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="chat", description="一個人太孤單嗎？")
    @app_commands.describe(context="說些話吧")
    async def chat(self, interaction: discord.Interaction, context: str):
        await interaction.response.defer()

        try:
            reply = chat_model.ollama_chat(context, model="qwen3.5:2b")

            if len(reply) > 3900:
                reply = reply[:3900] + "\n...（回覆過長已截斷）"

            embed = discord.Embed(
                title="小糖漿ㄉ回覆",
                description=reply or "模型沒有回覆內容。",
                color=discord.Color.green()
            )

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"嗚嗚嗚人家想不出來啦：{e}")

async def setup(bot):
    await bot.add_cog(Chat(bot))