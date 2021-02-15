from discord.ext.commands import Cog,command, has_permissions
from discord import Color, User, Embed
from discord.ext.commands import BucketType, CommandOnCooldown, cooldown,Greedy
from discord.ext.commands import CommandOnCooldown
class Mod(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.list_of_admins =[426549783864279040,
                             738990452673478738,
                             534074998672064512,]
    
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
            embed = discord.Embed(title = "Command: poo.warn",
                                description = '''**Description**: Warns a member
                                                **Cooldown**: 5 seconds
                                                **Usage**: poo.warn [member][reason]
                                            **CAN ONLY BE USED BY MODS**''',
                                color = discord.Color.dark_blue())
            await ctx.send(embed=embed)
            print(error)

def setup(bot):
    bot.add_cog(Mod(bot))