import discord
from discord.ext.commands import command,Cog
from discord_slash import cog_ext, SlashContext,SlashCommand

class Slash(Cog):
    def __init__(self, bot):
        pass
        

        if not hasattr(bot, "slash"):
         
            bot.slash = SlashCommand(bot,sync_commands = True,override_type=True)
       
        
        self.bot = bot

        self.bot.slash.get_cog_commands(self)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("slash")

    guild_ids = [711044562650398721,821513106403360809]
    @cog_ext.cog_slash(name="ping", guild_ids=guild_ids)
    async def ping(self, ctx: SlashContext):
        await ctx.send(content="Pong!")

def setup(bot):
    bot.add_cog(Slash(bot))