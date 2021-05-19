from datetime import datetime, timedelta
from random import randint
from typing import Optional

from discord import Member, Embed
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions
from discord.ext.menus import MenuPages, ListPageSource

from ..db import db
from .botmod import isBotAdmin






class Birthday(Cog):
    def __init__(self,bot):
        self.bot = bot

    
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("image")


    @command(name = "setBday",brief = "literally does nothing rn")
    @isBotAdmin
    async def setBday(self,ctx,img):
        pass



def setup(bot):
    bot.add_cog(Birthday(bot))


