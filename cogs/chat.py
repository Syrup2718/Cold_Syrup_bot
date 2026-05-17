import discord
from discord.ext import commands
from discord import app_commands
from services import chat_model

# 負責AI聊天

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_memory = {}

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
                key = (message.author.id, message.channel.id)
                messages = []

                # 1. 先拿短期記憶
                history = self.chat_memory.get(key, [])
                messages.extend(history)

                # 2. 如果這次是 reply，再把 reply chain 也補進來
                if message.reference:
                    reply_history = await self.build_reply_history(message, max_depth=10)
                    messages.extend(reply_history)

                # 3. 加上這次使用者輸入
                messages.append({"role": "user", "content": content})

                reply = chat_model.ollama_chat(messages, model="gemma4:e2b")

                if len(reply) > 3900:
                    reply = reply[:3900] + "\n...（回覆過長已截斷）"

                await message.reply(reply)

                # 4. 更新短期記憶
                history.append({"role": "user", "content": content})
                history.append({"role": "assistant", "content": reply})
                self.chat_memory[key] = history[-10:]   # 只留最近 10 則

            except Exception as e:
                print("出事情惹：", e)
                await message.reply("嗚嗚嗚人家想不出來啦")

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