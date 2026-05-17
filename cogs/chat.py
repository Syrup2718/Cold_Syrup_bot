import discord
from discord.ext import commands
from discord import app_commands
from services import chat_model

# 負責AI聊天

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def build_reply_history(self, message: discord.Message, max_depth: int = 10):
        history = []
        current = message
        depth = 0

        while current.reference and depth < max_depth:
            try:
                replied = current.reference.resolved

                if replied is None:
                    replied = await current.channel.fetch_message(current.reference.message_id)

                if replied.author.id == self.bot.user.id:
                    role = "assistant"
                else:
                    role = "user"

                content = replied.content.strip()
                if content:
                    if replied.author.id == self.bot.user.id:
                        history.append({
                            "role": role,
                            "content": content
                        })
                    else:
                        cleaned = content.replace(f"<@{self.bot.user.id}>", "")
                        cleaned = cleaned.replace(f"<@!{self.bot.user.id}>", "")
                        cleaned = cleaned.strip()

                        if cleaned:
                            history.append({
                                "role": role,
                                "content": cleaned
                            })

                current = replied
                depth += 1

            except Exception as e:
                print("抓回覆鏈失敗：", e)
                break

        history.reverse()
        return history

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.bot.user not in message.mentions:
            return

        content = message.content.replace(f"<@{self.bot.user.id}>", "")
        content = content.replace(f"<@!{self.bot.user.id}>", "")
        content = content.strip()

        if not content:
            await message.reply("嗷？泥在找窩嘛？")
            return

        async with message.channel.typing():
            try:
                messages = []

                if message.reference:
                    history = await self.build_reply_history(message, max_depth=10)
                    messages.extend(history)

                messages.append({"role": "user", "content": content})

                reply = chat_model.ollama_chat(messages, model="gemma4:e2b")

                if len(reply) > 3900:
                    reply = reply[:3900] + "\n...（回覆過長已截斷）"

                await message.reply(reply)

            except Exception as e:
                print("出事情惹：", e)
                await message.reply(f"嗚嗚嗚人家想不出來啦")

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
            print("出事情惹：", e)
            await interaction.followup.send(f"嗚嗚嗚人家想不出來啦")

async def setup(bot):
    await bot.add_cog(Chat(bot))