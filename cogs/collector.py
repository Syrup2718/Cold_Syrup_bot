import re
import discord
from discord.ext import commands
from database.message_repository import insert_msg

class Collector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def should_store_msg(self, message: discord.Message):
        if message.author.bot:
            return False

        if message.guild is None:
            return False
        
        content = message.content.strip()
        
        if not content:
            return False
        
        if re.fullmatch(r"https?://\S+", content):
            return False
        
        return True

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.should_store_msg(message):
            return
        
        insert_msg(
            message_id=str(message.id),
            guild_id=str(message.guild.id),
            channel_id=str(message.channel.id),
            author_id=str(message.author.id),
            author_name=message.author.display_name,
            content=message.content.strip(),
            created_at=message.created_at.isoformat()
        )
    
async def setup(bot):
    await bot.add_cog(Collector(bot))