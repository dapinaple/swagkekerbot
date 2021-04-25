from apscheduler.triggers.cron import CronTrigger
from discord import Color, Embed, Member, Permissions, User
from discord.ext.commands import (BucketType, Cog, CommandOnCooldown, Greedy,
                                  check, command, cooldown,
                                  has_guild_permissions, has_permissions)

from ..db import db
from datetime import datetime



list_of_admins = [426549783864279040]
def isBotAdminP(ctx):
    return ctx.author.id in list_of_admins

isBotAdmin = check(isBotAdminP)

class BotMod(Cog):
    def __init__(self,bot):
        self.bot = bot
        bot.scheduler.add_job(self.checkdayssince, CronTrigger(hour = '*/4'))
        
        
   
                
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("BotMod")


    
    async def checkdayssince(self):
        date = db.record("SELECT dateOfFunny FROM modusage")[0]

        date = datetime.strptime(date,'%Y-%m-%d').date()

        dayssince = datetime.now().date()-date

        channel = await self.bot.fetch_channel(835365059499786240)

        msg = await channel.fetch_message(835365240468275261)

        embed = Embed(title = "Days since the Funny",description=str(dayssince.days),color = Color.dark_blue())
        embed.set_thumbnail(url = channel.guild.icon_url)
        print(datetime.now().date()-date)
        print(dayssince.days)

        await msg.edit(embed = embed)

    @command(name = "reloadcog",brief = "reloads a cog of the bot\n**BOT OWNER USAGE ONLY**")
    @isBotAdmin
    async def reloadcog(self,ctx,cog):
        print(f'reloading lib.cogs.{cog}')
        self.bot.reload_extension(f'lib.cogs.{cog}')
        
        
            

    @command(name = "funnyhappen",brief = "Changes days since the funny.\n**BOT OWNER USAGE ONLY**")
    @isBotAdmin
    async def funnyhappen(self,ctx):
        db.execute('UPDATE modusage SET dateOfFunny = ? WHERE daysSinceFunny = ?',datetime.now().date(),1)
        
        db.commit()

    @command(name = "setprefix",brief = "sets the servers command prefix")
    @has_guild_permissions(administrator=True)
    async def setprefix(self,ctx,prefix: str):
        db.execute('UPDATE guilds SET Prefix = ? WHERE GuildID = ?',prefix,ctx.guild.id)
        db.commit()
    
    @command(name = "getprefix",brief = "gets the servers command prefix")
    async def getprefix(self,ctx):
        prefix = db.field('SELECT Prefix FROM guilds WHERE GuildID = ?',ctx.guild.id)
        await ctx.send(f'The prefix for this server is "{prefix}"')


        
        

def setup(bot):
    bot.add_cog(BotMod(bot))
