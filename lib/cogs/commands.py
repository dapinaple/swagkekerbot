from discord.ext.commands import command, Cog,has_permissions
from random import choice
class Commands(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bannedMembers = [438809594291027969,
                             227090540771016706]          

    
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("commands")


    @has_permissions(manage_messages = True)
    @command(name = "clear")
    async def clear(self,ctx,amount = 10):
        if ctx.author.id in self.bannedMembers:  
            await ctx.send("stfu")
        else:
            list_of_responses =["NO CLIPPING FOR YOU","JUST SAVED YOUR ASS","WHAT THE HELL WAS THAT"]
            if amount > 150 and ctx.author.id not in list_of_admins:
                await ctx.send("HELL NO THATS A LOT OF SHIT")
            else:
                await ctx.channel.purge(limit = amount + 1)

                await ctx.channel.send("***{}***".format(choice(list_of_responses)))

                
    @command(name = "ping",brief = "")
    async def ping(self,ctx):
        await ctx.send(f"**PONG** {round(self.bot.latency * 1000)}ms")
def setup(bot):
    bot.add_cog(Commands(bot))