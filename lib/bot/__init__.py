import asyncio
import os
import random
import string
import time
from datetime import date, datetime
from glob import glob

import discord
import pyfiglet
import pytz
import youtube_dl
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Intents, Member, guild
from discord.ext import commands, tasks
from discord.ext.commands import (BadArgument, Bot, BucketType,
                                  CommandNotFound, CommandOnCooldown,
                                  MissingRequiredArgument, cooldown,
                                  when_mentioned_or)
from discord.permissions import Permissions
from discord.utils import get
from discord.voice_client import VoiceClient
from discord_slash import SlashCommand
from pytz import timezone

from ..db import db

Intents.members = True
Intents.typing = True
Intents.messages = True
Intents.guilds = True




#ONLY TO TEST IF THE BOT IS ONLINE OKKKK
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

def get_prefix(bot,message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot,message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self,cog,True)
        print(f"{cog} cog ready")
    
    def all_ready(self):
        return all([getattr(self,cog)for cog in COGS])

class MainBot(Bot):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        
        self.guild = None
        self.scheduler = AsyncIOScheduler()

       # USING THE DATABASE.
        try:
            with open("./data/banlist.txt","r",encoding ="utf-8")as f:
                self.banlist=[int(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            self.banlist=[]
        db.autosave(self.scheduler)

        super().__init__(command_prefix=get_prefix,intents = discord.Intents.all())
        
        
        

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"cog {cog} loaded")
        print("setup complete")

    def run(self):
        print("running setup...")
        self.setup()
        
        self.token = 'NzM4OTkwNDUyNjczNDc4NzM4.XyT8fQ.vykBvcqIUc1ZSlemFYetHrY7tBU'
        print("running bot")
        super().run(self.token,reconnect = True)
    
    async def on_connect(self):
        print("bot connected")
    async def on_disconnect(self):
        ("bot disconnected")
    async def on_error(self,err,*args,**kwargs):
        if err =='on_command_error':
            await args[0].send("Something went wrong...")
        
        await self.stdout.send("an error occured")
        raise
    async def on_command_error(self, ctx, exc):
	    if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
		    pass


    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
					 ((guild.id,) for guild in self.guilds))
        db.multiexec("INSERT OR IGNORE INTO users (UserID) VALUES (?)",
                    ((user.id,) for user in self.users if not user.bot))
        db.commit()
        

    async def on_ready(self):
        
      if not self.ready:
        self.stdout = self.get_channel(800636861793304606)
        
        await asyncio.sleep(0.5)
        self.ready = True
        self.scheduler.start()


        self.update_db()

       
        ascii_banner = pyfiglet.figlet_format("Poopshitter has awoken")
        print(ascii_banner)
        print("Coded by Esteban \"Chief\" Schmitt on October 9th 2020\n")
        print("Operating in: \n")
        numguilds = 0



        for guild in self.guilds:
            print(f"{guild}")
            numguilds+=1
        print(f"I am in {numguilds} servers")
            
        print("\nCurrently keking  gnards")
        print("bot ready")

        meta = self.get_cog("Meta")
        await meta.set()

      else:
          print("bot reconnected")

    
    
bot = MainBot()


  
# # FUTURE ESTEBAN YOU NEED TO MAKE THE QUEUE WORK FOR THE PLAY FUNCTION
# # TRY MAKING SOME KIND OF WHILE LOOP BEFORE THE PLAYER FUNCTION OF AFTER IDK 
# # I DONT FUCKING KNOW DUDE IT DOESN'T MAKE SENSE -Esteban

# # YO WHATS UP GUYS WINTER BREAK STARTED POGGGGGG AND I DON'T WANNA MAKE THE QUEUE BC FUCK THAT -Chief

# #yo its 12:00 am rn on christmas day and I'm pogging rn.-esteba
# # Future esteban maybe we should make a holiday thing where the bot says something like "merry christmas", on a holiday
#  #              someones bday maybe>???? - eban

#  #shit good idea man - eban

#  # thanks dude - chief
 
#  # ye its a no on the holiday shit - chief
 

#  # work on the ban shit -eban 1.07

#  #THE BAN THING WORKSS PGGG -chief 1.16.21

#  # PURGE COMMAND WORKS AND IT ALSO ONLY LETS CERTAIN PPL USE IT LETS GOOOO POGGG - chief 1.18.21

#  # should prohbs focus on the IRR - eban 1.18.21

#  # stfu 1.18.21

# # REMEMBER TO ADD TO THE HELP COMMANDS TO DM ADMINS OF THE BOT - eban 1.18.21

# # binguscord raid success over 3.5k people banned, they shall never forget my name -cheif 1.20.21


         

     
    

   
    




        
















    



















    
# #run on server
# client.run('NzM4OTkwNDUyNjczNDc4NzM4.XyT8fQ.vykBvcqIUc1ZSlemFYetHrY7tBU')
    

