from discord.ext.commands import Cog
from discord.ext.commands import command
from apscheduler.triggers.cron import CronTrigger

from discord import Activity, ActivityType,Embed
class Meta(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.message = "Bot Under construction"

        # bot.scheduler.add_job(self.set, CronTrigger(second=5))
    
    
    
    
    async def set(self):
        _type, _name = self.message.split(' ',maxsplit = 1)

        await self.bot.change_presence(activity = Activity(

        name = _name,
        type = getattr(ActivityType,_type,ActivityType.listening)
        ))
        

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("meta")
    
def setup(bot):
    bot.add_cog(Meta(bot))