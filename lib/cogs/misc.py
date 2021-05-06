from random import choice
from typing import Optional

from discord import Color, Embed, Member
from discord.ext.commands import Cog, command, has_permissions
from pytz import timezone
from ..db import db



class Commands(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bannedMembers = [438809594291027969,
                             227090540771016706]

        self.fmt = "%a, %b %d, %Y %I:%M %p"                    
        self.list_of_admins = [426549783864279040]  
        self._max_clear = 300        

    
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")






    @has_permissions(manage_messages = True)
    @command(name = "clear",brief = "Clears the chat of 10 or <amount> messages\nWhen deleting a member's messages, it will delete **all messages up to 2 weeks prior** to the clear command")
    async def clear(self,ctx,member: Optional[Member], amount=10):
        
        if ctx.author.id in self.bannedMembers:  
            await ctx.send("stfu")
        else:
            list_of_responses =["GONE LIKE THE SENSE OF SMELL","CHAT IS GONE","DESTROYED BEYOND MAX BELIEF","OBLITERATED THE CHAT "]
            if amount > self._max_clear and ctx.author.id not in self.list_of_admins:
                await ctx.send("HELL NO THATS A LOT OF SHIT")

            else:
                await ctx.channel.purge(limit = amount+1 if not member else None, check = lambda message: message.author == member if member else True)

                await ctx.channel.send("***{}***".format(choice(list_of_responses)))
              
    

                    


                  
    @command(name = "ping",brief = "Gets the connection of something idk")
    async def ping(self,ctx):
        await ctx.send(f"**PONG** {round(self.bot.latency * 1000)}ms")
   
    @command(name = "dav1", brief = "Checks if you are the infamous Dav1")
    async def dav1(self,ctx):
        if ctx.author.id == 438809594291027969:
            await ctx.send("***OH GOD ITS YOU MOTHERFUCKING BITCH***")
        else:
            await ctx.send(":pensive:***no...you're not him***")

    @command(name = "getpfp",brief = "Gets the users pfp")
    async def getpfp(self,ctx, member: Member = None):
        if not member:
            member = ctx.author
            await ctx.send(member.avatar_url)
        else:
            await ctx.send(member.avatar_url)

    #JACKKKKKKKKKKKKKKKK
    @command(name = "jack",brief = "'tis jack")
    async def jack(self,ctx):
        if ctx.author.id in self.bannedMembers:
                await ctx.send("nope")
        else:
            await ctx.send("https://cdn.discordapp.com/attachments/800636511002427432/837699390860427284/unknown.png    ")
    # #8 BALLLLLLLLLLLLLLLLLLL

    @command(name = '_8ball', brief = "predicts the future with 100% accuracy.",aliases= ["8ball"])
    async def _8ball(self,ctx,*,message = None):
        if not message:
            await ctx.send("***U gonna say something orrr.....***")
        
        else:


            if ctx.author.id in self.bannedMembers:
                await ctx.send("***GET AWAY FROM ME IM NOT TELLING YOU SHIT***")
            else:
                responses =['totally ',
                        'yeah seems like it',
                        'absolutely man that\'s kek',
                        'heck yeah poggles',
                        'i\'d count on it tbh',
                        'fo sho my kek',
                        'yeah probably',
                        'looking pretty kek ngl',
                        'indubitably',
                        'what kind of quesiton is that of course',
                        'my bad i was eatin tacos, can u repeat?',
                        'eh i don\'t wanna answer now',
                        'ohhh i can\'t tell u now it\'ll ruin it',
                        'im gone man ask later',
                        'say agane',
                        "yeahhhh probably not",
                        'i don\'t think so dude',
                        'the homies say no sry',
                        'not looking too kek ',
                            'hell no']
                response = choice(responses)

                await ctx.send(response)
                print(f"{ctx.author.name} asked poopshitter: {message}")       
    @command(name = "flip",brief ="flips a coin")
    async def flip(self,ctx):
        coin_flip = choice([0,1])
        if ctx.author.id in self.bannedMembers:
            await ctx.send("***GET THE FUCK AWAY FROM ME***")

        elif coin_flip == 0:
            await ctx.send("***Heads***")
        else:
            await ctx.send("***Tails***")   

    @command(name = "dylan",brief = "dylan")
    async def dylan(self,ctx):
        if ctx.author.id in self.bannedMembers:
               await ctx.send("nope")
        else:
            await ctx.send("https://cdn.discordapp.com/attachments/814191607057874944/814899965775708170/unknown.png")

    @command(name = "getservericon",brief = "sends the servers icon")
    async def getservericon(self,ctx):
        if ctx.author.id in self.bannedMembers:
            await ctx.send("no")
        else:
            await ctx.send(ctx.guild.icon_url)

    @command(name = "info",brief = "gets some info on a member")
    async def info(self,ctx, member: Optional[Member]):
        if not member:
            member = ctx.author
        embed = Embed(title = '',description = member.mention, inline = True,color = member.color)
        embed.set_author(name = member,icon_url= member.avatar_url)

       

        embed.add_field(name = "Joined", value = timezone("America/New_York").localize(member.joined_at).strftime(self.fmt))
        
        
        embed.add_field(name = "Account Created",value = timezone("America/New_York").localize(member.created_at).strftime("%a, %b %d, %Y %I:%M %p"))
        embed.set_thumbnail(url = member.avatar_url)
    
        embed.add_field(name = f"Roles[{len(member.roles)-1}]",value = ' '.join(str(r.mention) for r in member.roles[:0:-1]) if len(member.roles)>1 else "None", inline = False)

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Commands(bot))



