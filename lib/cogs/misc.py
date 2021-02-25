from discord.ext.commands import command, Cog,has_permissions
from random import choice
from discord import Member
class Commands(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bannedMembers = [438809594291027969,
                             227090540771016706]
        self.list_of_admins = [426549783864279040]          

    
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")


    @has_permissions(manage_messages = True)
    @command(name = "clear",brief = "Clears the chat of 10 or <amount> messages")
    async def clear(self,ctx,amount = 10):
        
        if ctx.author.id in self.bannedMembers:  
            await ctx.send("stfu")
        else:
            list_of_responses =["NO CLIPPING FOR YOU","JUST SAVED YOUR ASS","WHAT THE HELL WAS THAT"]
            if amount > 150 and ctx.author.id not in self.list_of_admins:
                await ctx.send("HELL NO THATS A LOT OF SHIT")
            else:
                await ctx.channel.purge(limit = amount + 1)

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
            await ctx.send("https://cdn.discordapp.com/attachments/747289514891804742/783757708486115358/unknown.png")
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
                print(f"{ctx.author.name} asked poopshitter = {message}")       
    @command(name = "flip",brief ="flips a coin")
    async def flip(self,ctx):
        coin_flip = choice([0,1])
        if ctx.author.id in self.bannedMembers:
            await ctx.send("***GET THE FUCK AWAY FROM ME***")

        elif coin_flip == 0:
            await ctx.send("***Heads***")
        else:
            await ctx.send("***Tails***")       
    @command(name = "getservericon",brief = "sends the servers icon")
    async def getservericon(self,ctx):
        if ctx.author.id in self.bannedMembers:
            await ctx.send("no")
        else:
            await ctx.send(ctx.guild.icon_url)
def setup(bot):
    bot.add_cog(Commands(bot))