from discord.ext.commands import Cog,command
from discord.utils import get
from discord import Embed, Color
from typing import Optional

def syntax(command):
    cmd_and_aliases = "|".join([str(command),*command.aliases])
    
    params = []
    # print(value for key,value in command.params.items())
    for key, value in command.params.items():
        if key not in ("self","ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)
    return f"''' {cmd_and_aliases} {params}'''"

class Help(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bot.remove_command("help")


    async def cmd_help(self,ctx,command):
        embed = Embed(title = f"Command `{command}` ",
                        description = syntax(command),
                        color = Color.dark_blue())
        embed.add_field(name = "Command description",value = command.help)
        await ctx.send(embed = embed)

    @command(name = "help",aliases = ["helpme","ineedhelp"])
    async def show_help(self,ctx,cmd:Optional[str]):
        """Shows this message"""
        if cmd is None:
            pass
        else:
            if(command := get(self.bot.commands,name=cmd)):
                await self.cmd_help(ctx,command)
            else:
                await ctx.send("That command does not exist.")


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")


def setup(bot):
    bot.add_cog(Help(bot))
