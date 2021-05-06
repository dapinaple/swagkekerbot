from apscheduler.triggers.cron import CronTrigger
from discord import Color, Embed, Member, Permissions, User
from discord.ext.commands import (BucketType, Cog, CommandOnCooldown, Greedy,
                                  check, command, cooldown,
                                  has_guild_permissions, has_permissions,ChannelNotFound)

from ..db import db
from datetime import datetime
from typing import Optional



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

        channel = self.bot.get_channel(835365059499786240)

        msg = channel.get_partial_message(835365240468275261)

        embed = Embed(title = "Days since the Funny",description=str(dayssince.days),color = Color.dark_blue())
        embed.set_thumbnail(url = channel.guild.icon_url)

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
        await self.checkdayssince()
        db.commit()

    @command(name = "setprefix",brief = "sets the servers command prefix")
    @has_guild_permissions(administrator=True)
    async def setprefix(self,ctx,prefix: str):
        db.execute('UPDATE guilds SET Prefix = ? WHERE GuildID = ?',prefix,ctx.guild.id)
        db.commit()

    @command(name = "setghost",brief = "sets the ghost ping channel to the current channel")
    @has_guild_permissions(administrator = True)
    async def setghost(self,ctx):

        ghostID =  ctx.channel.id
        
            

        db.execute('UPDATE guilds SET ghostID = ? WHERE GuildID = ?',ghostID,ctx.guild.id)
        db.commit()
    
    @command(name = "getprefix",brief = "gets the servers command prefix")
    async def getprefix(self,ctx):
        prefix = db.field('SELECT Prefix FROM guilds WHERE GuildID = ?',ctx.guild.id)
        await ctx.send(f'The prefix for this server is "{prefix}"')

    @command(name = "getguildid",brief = "gets guildname from id",hidden =True)
    async def getguild(self,ctx,guildid: int):
        print(self.bot.get_guild(guildid))

    @command(name = "tempunban",brief = "unbans from a guild ",hidden = True)
    @isBotAdmin
    async def unban(self,ctx, id: int,guildid: int):
        
        user = self.bot.get_user(id)
        guild = self.bot.get_guild(guildid)
        await guild.unban(user)
        print(f"unbanned {user.name}")
    
    @command(name = "createinv",brief ="creates invite to a server",hidden = True)
    @isBotAdmin
    async def createinv(self,ctx,guildID: int):
        guild = self.bot.get_guild(guildID)
        channel = guild.channels[0]
        await ctx.author.send( await channel.create_invite())
       

        
        

def setup(bot):
    bot.add_cog(BotMod(bot))
