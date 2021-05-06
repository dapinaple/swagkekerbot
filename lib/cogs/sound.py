from random import choice
from typing import Optional

from discord import Color, Embed, Member
from discord.ext.commands import Cog, command, has_permissions,has_any_role
from .botmod import isBotAdmin


class Sound(Cog):
    def __init__(self,bot):
        self.bot = bot       

    
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("sound")


    
    @client.command(name='join', help='Calls the bot to join a voice channel')
    async def join(self,ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return

        else:
           channel = ctx.message.author.voice.channel

        await channel.connect()
        

        

    
def setup(bot):
    bot.add_cog(Sound(bot))