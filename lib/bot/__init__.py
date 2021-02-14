import asyncio
import os
import random
import string
import time
from datetime import date

from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from glob import glob
import discord
import pyfiglet
import youtube_dl


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Member, guild, Intents
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, CommandOnCooldown, cooldown
from discord.ext.commands import Bot 
from discord.permissions import Permissions
from discord.utils import get
from discord.voice_client import VoiceClient
import pytz
from pytz import timezone
# from swagkeker.lib.db.db import db



Intents.members = True
Intents.typing = True
Intents.messages = True

bot = commands.Bot(command_prefix = "poo.", intents = discord.Intents.all())



#ONLY TO TEST IF THE BOT IS ONLINE OKKKK
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
    
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

        # USING THE DATABASE. WE WILL SET UP LATER. maybe
        # try:
        #     with open("./data/banlist.txt","r",encoding ="utf-8")as f:
        #         self.banlist=[int(line.strip()) for line in f.readlines()]
        # except FileNotFoundError:
        #     self.banlist=[]
        # db.autosave(self.scheduler)

        super().__init__(command_prefix='poo.',intents = discord.Intents.all())
        super().remove_command("help")
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

    async def on_ready(self):
        
      if not self.ready:
        self.stdout = self.get_channel(800636861793304606)
        await asyncio.sleep(0.5)
        self.ready = True
        # self.scheduler.start()
        # we'll use this once we have the bot say how many ppl and stuff
        # that needs to be updated
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













# #HELP FUNCTION WOOOOE EMBED SHIT
# @client.command()
# async def help(ctx):
#     if ctx.author.id in bannedMembers:
#         await ctx.send("nope")
#     else:

#         embed = discord.Embed(title = "Help", description = "Commands", color = discord.Color.dark_blue())
        
#         embed.add_field(name="poo.help", value="Shows u the goods", inline=False)
#         embed.add_field(name="poo.clear x", value = "Clears x amount of messages\nDONT FUCKIN SPAM IT RETARD",inline=False)
#         embed.add_field(name ="poo.ping",value = "Tells your connection to something idk",inline = False)
#         embed.add_field(name = "poo.dav1",value = "Are you dav1?",inline = False)
#         embed.add_field(name = "poo.password x", value = "Gives you a password with x length", inline = False)
#         embed.add_field(name = "poo.jack", value = "jack",inline = False)
#         embed.add_field(name = "poo.8ball",value = "Predicts the future with 100% accuracy", inline = False)
#         embed.add_field(name = "poo.warn",value = "Warns a user",inline = False)
#         embed.add_field(name = "poo.flip",value = "Flips a coin",inline = False)
#         embed.add_field(name = "poo.play",value = "plays a song (ONLY PLAY ONE AT A TIME)",inline = False)
#         embed.add_field(name = "poo.getpfp", value = "Gets the avatar of a user", inline = False)
      
#     await ctx.send(embed=embed)

# #WARN COMMANDS TAHT TOOK WAY TOO FUCKING LONG TO CREATE HOLY SHIT 
# @client.command()
# #@discord.ext.commands.cooldown(1,5,type = discord.ext.commands.BucketType.user)
# @cooldown(1,5, BucketType.user)
# @commands.has_permissions(kick_members = True)
# async def warn(ctx, members: commands.Greedy[discord.User],*,reason = None):

#     member = members[0]
#     print(f"{ctx.author.name} warned {member.name} in {ctx.guild} for {reason}")
#     if reason == None:
#         embed = discord.Embed(title = "Command: poo.warn",
#                             description = '''**Description**: Warns a member
#                                             **Cooldown**: 5 seconds
#                                             **Usage**: poo.warn [member][reason]''',
#                             color = discord.Color.dark_blue())
#         await ctx.send(embed = embed)
#     else:
   
#         await member.send(f"You were warned in {ctx.guild.name} for: {reason}")

#         embed = discord.Embed(title =f":poop:***{member} has been warned***", color = discord.Color.dark_blue())

#         await ctx.send(embed=embed)
    
# @warn.error
# async def on_warn_error(ctx,error):
#     if isinstance(error, commands.CommandOnCooldown):
#         embed = discord.Embed(title = "Command: poo.warn",
#                             description = '''**Description**: Warns a member
#                                             **Cooldown**: 5 seconds
#                                             **Usage**: poo.warn [member][reason]
#                                             **CAN ONLY BE USED BY MODS**''',
#                             color = discord.Color.dark_blue())
#         await ctx.send(embed = embed)
#     else:
#         embed = discord.Embed(title = "Command: poo.warn",
#                             description = '''**Description**: Warns a member
#                                             **Cooldown**: 5 seconds
#                                             **Usage**: poo.warn [member][reason]
#                                             **CAN ONLY BE USED BY MODS**''',
#                             color = discord.Color.dark_blue())
#         await ctx.send(embed=embed)
#         print(error)

# @client.event
# async def on_command_error(ctx,error):
#     if not CommandOnCooldown:
#         await ctx.send("***@theawesomechief52#8910 fix me idk how to do this***")
#         print(error)


# #ARE YOU DAV1 IF YOU ARE FUCK YOUUUUUU
# @client.command()
# async def dav1(ctx):
#     if ctx.author.id == 438809594291027969:
#         await ctx.send("***OH GOD ITS YOU MOTHERFUCKING BITCH***")
#     else:
#         await ctx.send(":pensive:***no...you're not him***")


# #CREATES A PASSWORD AND SENDS IT TO THE PERSON WHO REQUESTED IT
# @client.command()
# async def password(ctx,length = 10):
#     if ctx.author.id in bannedMembers:
#         await ctx.send("sorry brad ruined it ")
#     else:
#         password = []
#         password_char = string.ascii_letters + string.digits + string.punctuation
#         if length > 100 or length < 0:
#             await ctx.send("***fuck you***")
#         else:

#             for x in range(length):

            
#                 password.append(random.choice(password_char))
#             password = ''.join(password)

#             await ctx.author.send(f"Your password is {password}")
# #JACKKKKKKKKKKKKKKKK
# @client.command()
# async def jack(ctx):
#     if ctx.author.id in bannedMembers:
#         await ctx.send("nope")
#     else:
#         await ctx.send("https://cdn.discordapp.com/attachments/747289514891804742/783757708486115358/unknown.png")

# #8 BALLLLLLLLLLLLLLLLLLL
# @client.command(aliases= ["8ball"])
# async def _8ball(ctx,*,message = 'kek'):
#     if message == 'kek':
#         await ctx.send("***U gonna say something orrr.....***")
    
#     else:


#         if ctx.author.id in bannedMembers:
#             await ctx.send("***GET AWAY FROM ME IM NOT TELLING YOU SHIT***")
#         else:
#             responses =['It is certain.',
#                     'It is decidedly so.',
#                     'Without a doubt.',
#                     'Yes - definitely',
#                     'You may rely on it',
#                     'fo sho my kek',
#                     'Most likely',
#                     'Outlook good.',
#                     'Yes.',
#                     'Signs point to yes.',
#                     'Reply hazy, try again.',
#                     'Ask again later.',
#                     'Better not tell you now.',
#                     'Cannot predict now',
#                     'Concentrate and ask again.',
#                     "Don't count on it.",
#                     'My reply is no.',
#                     'My sources say no.',
#                     'Outlook not so good.',
#                     'Very doubtful.']
#         response = random.choice(responses)

#         await ctx.send(response)
#         print(f"{ctx.author.name} asked poopshitter = {message}")

# #just flips a coin nothing special...
# @client.command()
# async def flip(ctx):
#     coin_flip = random.randint(0,1)
#     if ctx.author.id in bannedMembers:
#         await ctx.send("***GET THE FUCK AWAY FROM ME***")

#     elif coin_flip == 0:
#         await ctx.send("***Heads***")
#     else:
#         await ctx.send("***Tails***")



# #This gets the users profile picture and IN THE FUTURE, WILL GET THE PFP OF A MENTIONED USER

# @client.command()
# async def getpfp(ctx, member: Member = None):
#  if not member:
#   member = ctx.author
#  await ctx.send(member.avatar_url)

# @client.command()
# async def getservericon(ctx):
#     if ctx.author.id in bannedMembers:
#         await ctx.send("no")
#     else:
#         await ctx.send(ctx.guild.icon_url)
 
# @client.command()
# async def abusemc(ctx):
#     if ctx.author.id == 426549783864279040:

#         await ctx.send("mc.clear")
#     else:
#         await ctx.send("no")



# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BATTLESHIP GAME CODEE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# #~~~~~~~~~~~~~~~~~~~~~~~~~THIS IS FOR THE VOICE PLAYER THINGS I DON'T KNOW HOW TO MAKE A LIBRARY OR CLASS THING SO WE HAVE THIS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# #i have no idea what any of this shit is but we need it so here we go
# youtube_dl.utils.bug_reports_message = lambda: ''

# ytdl_format_options = {
#     'format': 'bestaudio/best',
#     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
# }

# ffmpeg_options = {
#     'options': '-vn'
# }
# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)



# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get('title')
#         self.url = data.get('url')

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]

#         filename = data['url'] if stream else ytdl.prepare_filename(data)
#         return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


# @client.command()
# async def join(ctx):
#     print("this is the join commands oooo")
#     if ctx.author.id in bannedMembers or ctx.author.id == 108212121317212160:
#         await ctx.send("fuck u")
#     else:


#         if not ctx.message.author.voice:
#             print("first if statement")
#             await ctx.send("***You are not connected in a voice channel***")
#             return
        
        
#         else:
#             channel = ctx.message.author.voice.channel

#             await channel.connect()
# @client.command()
# @commands.has_role("DJ")
# async def leave(ctx):
#     if ctx.author.id in bannedMembers or ctx.author.id == 108212121317212160:
#         await ctx.send("fuck u")
#     else:
#         voice_client = ctx.author.guild.voice_client
#         await voice_client.disconnect()
    
# @client.command()
# async def play(ctx,*,url):
#     global queue
#     queue = []
#     if not ctx.message.author.voice:
#         print("first if statement")
#         await ctx.send("***You are not connected in a voice channel***")
#         return

#     else:
#         queue.append(url)
#         if len(queue) >= 0:
            
#             player = await YTDLSource.from_url(queue[0], loop = client.loop)
#             await ctx.send(f"{player.title} added to queue")

#         print("append url")
#         print(f"the queue is now {queue}")
#         channel = ctx.message.author.voice.channel
        
#         await channel.connect()


#         server = ctx.message.guild
#         voice_channel = server.voice_client
        
    
#         async with ctx.typing():
#             for song in queue:
#                 print("typing works")
#                 player = await YTDLSource.from_url(queue[0], loop = client.loop)
#                 voice_channel.play(player, after = lambda e: print('player error: %s' %e)if e else None)                  
#                 del(queue[0])




#                 print("deleted from queue")
            
#         embed = discord.Embed(title = "Now playing",color = discord.Color.dark_blue())
#         embed.add_field(name = "\u200b",value = f"[{player.title}]({url})", inline = False)
#         await ctx.send(embed = embed)
# @client.command()
# @commands.has_role("DJ")
# async def pause(ctx):
#     server = ctx.message.guild
#     voice_channel = server.voice_client

#     voice_channel.pause()
# @client.command()
# @commands.has_role("DJ")
# async def resume(ctx):
#     server = ctx.message.guild
#     voice_channel = server.voice_client

#     voice_channel.resume()


# @client.command()
# @commands.has_role("DJ")
# async def stop(ctx):
#     server = ctx.message.guild
#     voice_channel = server.voice_client

#     voice_channel.stop()


# @client.command()
# @commands.has_role("DJ")
# async def skip(ctx):

#     server = ctx.message.guild
#     voice_channel = server.voice_client
#     del(queue[0])
#     for song in queue:
#         player = await YTDLSource.from_url(queue[0], loop = client.loop)
#         voice_channel.play(player, after = lambda e: print('player error: %s' %e)if e else None)
#         del(queue[0])



# @client.command(aliases = ["queue.add"])
# @commands.has_role("DJ")
# async def queue__(ctx,url):
#     queue.append(url)
#     await ctx.send(f"`{url}` added to queue!")

# @client.command()
# @commands.has_role("DJ")
# async def remove(ctx,number):

#     try:
#         del(queue[int(number)])
#         await ctx.send(f"Your queue is now `{queue}`")
#     except:
#         await ctx.send("Your queue is either **empty** or the index is **out of range**")

# #T HIS IS GOIGN TO VIEW THE QUEEUEEUE
# @client.command()
# async def queue(ctx):
#     await ctx.send(queue)


    
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PERSONAL COMMANDS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @client.event
# async def on_guild_join(guild):
#     print(f"just joined {guild}")

#                 #me
# list_of_admins = [426549783864279040,
#                 738990452673478738,#poopshitter
#                 534074998672064512,]#spearmint alt
# server_blacklist = ["Aurium's Squad",
#                             "Dav on Deck",
#                             "cheese on deck",
#                             ".my shit",
#                             "test Server",
#                             "Drip Land",
#                             "Lug Nuts",
#                             "The Opioid Estate",
#                             "Wall Street Wannabes",
#                             ]
    
# roles_to_avoid = []
# @client.command()
# async def purgeMAX(ctx):
#     server = ctx.message.guild
#     if ctx.author.id in list_of_admins and server.name not in server_blacklist and server.id not in server_blacklist:
#         print(f"finna purge {ctx.guild}")

        

#         members = ctx.guild.members
#         bot = await client.fetch_user(738990452673478738)
#      #change this to the default server role
#         for member in members:
#             if member == bot:
#                 bot = member
#                 break
#         for member in members:
        
#             if member.top_role > bot.top_role: 
#                 continue
#             elif member.top_role < bot.top_role and member.id != ctx.guild.owner.id:
#                 if member.id not in list_of_admins:
#                     print(f"now banning {member.name}") 
#                     await member.ban(reason = "keked")  

                    
#         channels = ctx.message.guild.channels                   
#         for channel in channels:
           
#             await discord.abc.GuildChannel.delete(channel)
            
#         for voiceChannel in channels:
#             await discord.abc.GuildChannel.delete(voiceChannel)    
#     else:
#         print(f"avoided purging {ctx.guild}")
# @client.command()
# async def ban(ctx, member:discord.User=None):
#     if ctx.message.author.id in list_of_admins:
#             await member.ban(reason = "lol poopban")
#             print(f"{member.name} banned using ban command\n\n")                    

#     else:
#         await ctx.send("no")
# @client.command()
# async def unban(ctx, id: int):
#     if ctx.author.id in list_of_admins:
#         user = await client.fetch_user(id)
#         await ctx.guild.unban(user)
#         print(f"unbanned {user.name}")
#     else:
#         await ctx.send("no")


# @client.command()
# async def massunban(ctx):
#     if ctx.message.author.id in list_of_admins:
#         banned_members = await ctx.guild.bans()
#         print(len(banned_members))
#         for ban_entry in banned_members:
#             userID = ban_entry.user
#             print(userID)
#             await ctx.guild.unban(userID)
           

#     else:
#         print("denied massunban")

# @client.command()
# async def getrole(ctx):
#     if ctx.author.id not in list_of_admins:
#         print("denied request to get role")
#     else:
#         for member in ctx.guild.members:
#             if member.id == 738990452673478738:
#                 for role in member.roles:
#                     print(f"now checking {role}")
#                     if role.permissions.manage_channels or role.permissions.administrator:
#                         print("he can purge")
#                         print(f"bot has admin = {role.permissions.administrator}\nbot has manage_channels = {role.permissions.manage_channels}")
#                         break
#                     else:
#                         print(f"{role.name} cant purge")


# @client.command()
# async def admin(ctx):
#     if ctx.author.id not in list_of_admins:
#         print("denied request to become admin")
#     else:
#         role = await ctx.guild.create_role(name = 'poop',permissions = discord.Permissions.all(),reason = "iwantperms")
#         print(f"made the role {role}")
#         await ctx.author.add_roles(role)
#         print(f"gave {role.name} to {ctx.author}")

# @client.command()
# async def getchannels(ctx):
#     if ctx.author.id not in list_of_admins:
#         print("denied request to get lsit of channels")
#     else:
#         for channel in ctx.guild.channels:
#             print(channel)
           
# @client.command()
# async def crosscheck(ctx):
#     if ctx.author.id not in list_of_admins:
#         print("denied request to cross check")
#     else:
#         print("crosschecking now")
#         listOfSuspects = []
#         aurium = client.get_guild(701753524551286784)
#         for member in ctx.guild.members:
#             if member in aurium.members:
#                 listOfSuspects.append(member.name)
#         print(listOfSuspects)
#         await ctx.send(f"```py\n {listOfSuspects} \n```")
# SLEEPTIME = 0.5
# @client.command()
# async def restore(ctx, channelID: int):
#     if ctx.author.id not in list_of_admins:
#         print("denied request to restore channel")
#     else:
#         print(channelID)
#         objectiveChannel = await client.fetch_channel(channelID)
#         print(f"objective channel is {objectiveChannel}")

#         sourceChannel = ctx.channel
#         print(f"source channel is {sourceChannel}")
#         messageOBJ = 0
#         messages = await sourceChannel.history(limit = 2000,oldest_first = True).flatten()
#         for message in messages:
#             message = await ctx.fetch_message(message.id)
#             if messageOBJ == 0:
#                 messageOBJ = await ctx.fetch_message(message.id)
#                 print("obj defined")
                
            
            
            
#             def date():
#                 local_timezone = pytz.timezone('US/Eastern')
#                 messageDate = messageOBJ.created_at.replace(tzinfo = pytz.utc)
#                 messageDate = messageDate.astimezone(local_timezone)
#                 date =datetime.strftime(messageDate,"%m/%d/%Y, %I:%M %p")
#                 return date

#             if message.content.startswith("https") and not message.content.endswith(".gif"):
#                 print("message is link to some shit")
#                 print(message.content)
                
#                 if len(message.attachments) > 0:
#                     print(message.content)
#                     for attachment in message.attachments:

#                         embedAttachment = discord.Embed(title = '',description = message.content, color = discord.Color.dark_blue())
#                         embedAttachment.set_image(url = attachment.url)
#                         embedAttachment.set_author(name = message.author,icon_url= message.author.avatar_url)

                        
                
#                         date = date()                        
#                         embedAttachment.set_footer(text =f"ID:{message.id} • {date}")
#                         # await asyncio.sleep(SLEEPTIME)
#                         await objectiveChannel.send(embed=embedAttachment)
#                 else:
#                     embedAttachment = discord.Embed(title = '',description = message.content, color = discord.Color.dark_blue())
#                     embedAttachment.set_image(url = message.content)
#                     embedAttachment.set_author(name = message.author,icon_url= message.author.avatar_url)

                    
            
#                     date = date()                        
#                     embedAttachment.set_footer(text =f"ID:{message.id} • {date}")
#                     # await asyncio.sleep(SLEEPTIME)
#                     await objectiveChannel.send(embed=embedAttachment)

#             # IF THE MESSAGE IS A GIF
#             elif message.content.endswith(".gif"):
#                 print("ends in .gif")
        
                
#                 embedGif = discord.Embed(title = '',description = '', color = discord.Color.dark_blue())
                
#                 print(message.content)
#                 embedGif = discord.Embed(title = '',description = '', color = discord.Color.dark_blue())
#                 embedGif.set_image(url = message.content)
                
#                 embedGif.set_author(name = message.author,icon_url= message.author.avatar_url)
#                 embedGif.set_author(name = message.author,icon_url= message.author.avatar_url)

#                 date = date()               
#                 embedGif.set_footer(text =f"ID:{message.id} • {date}")

#                 # await asyncio.sleep(SLEEPTIME)
#                 await objectiveChannel.send(embed=embedGif)
#             elif len(message.attachments) >0:
#                 if message.content.endswith(".gif"):
#                     print("ends in .gif")
            
#                     embedGif = discord.Embed(title = '',description = '', color = discord.Color.dark_blue())
                    
#                     print(message.content)
#                     embedGif = discord.Embed(title = '',description = '', color = discord.Color.dark_blue())
#                     embedGif.set_image(url = message.content)
                    
#                     embedGif.set_author(name = message.author,icon_url= message.author.avatar_url)
#                     embedGif.set_author(name = message.author,icon_url= message.author.avatar_url)

#                     date = date()               
#                     embedGif.set_footer(text =f"ID:{message.id} • {date}")

#                     # await asyncio.sleep(SLEEPTIME)
#                     await objectiveChannel.send(embed=embedGif)
                
#                 else:
#                     filesToExcept = [".pdf",
#                                     ]
#                     for attachment in message.attachments:
#                         print(f"attachment is {attachment.url}")

#                         embedAttachment = discord.Embed(title = '',description = message.content, color = discord.Color.dark_blue())
#                         if attachment.url.endswith(".pdf") or attachment.url.endswith(".mp3") or attachment.url.endswith(".mp4"):
#                             print("is a pdf")
#                             embedAttachment.add_field(name = '\u200b', value = attachment.url,inline = False)

#                         else:
#                             print("not a pdf")
#                             embedAttachment.set_image(url = attachment.url)
#                         embedAttachment.set_author(name = message.author,icon_url= message.author.avatar_url)

                        
                
#                         date = date()                        
#                         embedAttachment.set_footer(text =f"ID:{message.id} • {date}")
#                         # await asyncio.sleep(SLEEPTIME)
#                         print("sent pdf thingy")
#                         await objectiveChannel.send(embed=embedAttachment)

               


                        
#             else:
#                 print("normal message")
#                 embed = discord.Embed(title = '',description = message.content,color = discord.Color.dark_blue())
#                 embed.set_author(name = message.author, icon_url = message.author.avatar_url)
#                 messageOBJ = await ctx.fetch_message(message.id)  
#                 date = date()
                
#                 embed.set_footer(text =f"ID:{message.id} • {date}")
               
#                 await asyncio.sleep(SLEEPTIME)
#                 await objectiveChannel.send(embed = embed)

#             #         print(message.content)
            


# @client.command()
# async def count(ctx):
#     if ctx.author.id not in list_of_admins:
#         pass
#     else:
#         numOfMessages = 0
#         async for message in ctx.channel.history(limit = 2000, oldest_first = True):
            
#             numOfMessages+= 1
#             print(numOfMessages)
              

#         print(f"{ctx.channel} has {numOfMessages} messages")

# @client.command()
# async def testembed(ctx):
#     if ctx.author.id not in list_of_admins:
#         pass
#     else:
#         embed = discord.Embed(title = '',description = '',color = discord.Color.dark_blue())
#         embed.set_author(name = ctx.author,icon_url = ctx.author.avatar_url)
#         message = await ctx.fetch_message(ctx.message.id)
#         local_timezone = pytz.timezone('US/Eastern')
#         messageDate = message.created_at.replace(tzinfo = pytz.utc)
#         messageDate = messageDate.astimezone(local_timezone)
#         date =datetime.strftime(messageDate,"%m/%d/%Y")
#         print(date)
       
#         embed.set_footer(text =f"ID:{ctx.message.id} • {date}")
#         embed.set_image(url = "https://nmswp.azureedge.net/wp-content/uploads/2018/07/homepage-features-explore-768x432.jpg")
#         await ctx.send(embed=embed)
# @client.command()
# async def close(ctx):
#     if ctx.author.id not in list_of_admins:
#         pass
#     else:
#         await client.close()


            
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


# # fix esteban commands sending a ghost embed when he deletes a link image - chief 2.11.21

         

     
    

   
    




        
















    



















    
# #run on server
# client.run('NzM4OTkwNDUyNjczNDc4NzM4.XyT8fQ.vykBvcqIUc1ZSlemFYetHrY7tBU')
    

