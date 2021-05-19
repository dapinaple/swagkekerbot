from random import choice
from typing import Optional

from discord import Color, Embed, Member, DiscordException,VoiceChannel
from discord.ext.commands import Cog, command, has_permissions,has_any_role
from .botmod import isBotAdmin
import wavelink


class Music(Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

    
def setup(bot):
    bot.add_cog(Music(bot))