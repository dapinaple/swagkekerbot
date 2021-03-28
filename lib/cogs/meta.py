from discord.ext.commands import Cog
from discord.ext.commands import command
from apscheduler.triggers.cron import CronTrigger

from discord import Activity, ActivityType,Embed
class Meta(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.message = "Bot| poo.help"

        # bot.scheduler.add_job(self.set, CronTrigger(second=5))
    
    
    
    
    async def set(self):
        _type, _name = self.message.split(' ',maxsplit = 1)

        await self.bot.change_presence(activity = Activity(

        name = _name,
        type = getattr(ActivityType,_type,ActivityType.listening)
        ))

    @command(name = "load",brief = "loads an extension", hidden = True)
    async def load(self,ctx,*file):
        if ctx.author.id !=426549783864279040:
            pass
        else:
            pass

    @Cog.listener()
    async def on_guild_join(self,guild):
        print(f"I joined {guild}") 
    @Cog.listener()
    async def on_guild_remove(self,guild):
        print(f"I left {guild}") 
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("meta")
    
def setup(bot):
    bot.add_cog(Meta(bot))