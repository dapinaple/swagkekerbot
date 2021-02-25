from discord.ext.commands import Cog,command
from discord.utils import get
from discord import Embed, Color
from discord.ext.menus import MenuPages, ListPageSource
from typing import Optional

def syntax(command):
    cmd_and_aliases = "|".join([str(command),*command.aliases])
    
    params = []
    # print(value for key,value in command.params.items())
    for key, value in command.params.items():
        if key not in ("self","ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)
    return f"``` {cmd_and_aliases} {params}```"

class HelpMenu(ListPageSource):
    def __init__(self,ctx,data):
        self.ctx = ctx
        self.entries_to_remove = len([i for i in data if i.hidden == True])
        
        per_page = 3
        
        
        

        super().__init__(data,per_page=3)
        

        if self.ctx.author.id == 426549783864279040:
            self.hidden_items = per_page -1
        else:
            self.hidden_items = per_page -len([i for i in data if i.hidden == True]) 

    async def write_page(self,menu,fields=[]):
        offset = (menu.current_page*self.per_page)+1
        len_data = len(self.entries)-self.entries_to_remove
        
        
        embed = Embed(title = "Help",
                     description = "Poopshitter help dialog",
                     color = Color.dark_blue())
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.hidden_items):,} of {len_data:,} commands.")

        for name,value in fields:
            embed.add_field(name = f"poo.{value}", value = name, inline = False)
        
            

        return embed
    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            if entry.hidden == False or self.ctx.author.id == 426549783864279040:
                fields.append((entry.brief or "No description", syntax(entry)))
            else:
                
                continue
                
        return await self.write_page(menu,fields)


class Help(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bot.remove_command("help")
        self.show_hidden = False


    async def cmd_help(self,ctx,command):
        embed = Embed(title = f"Command `{command}` ",
                        description = syntax(command),
                        color = Color.dark_blue())
        embed.add_field(name = "Command description:",value = command.brief)
        await ctx.send(embed = embed)

    @command(name = "help",brief = "Shows this message")
    async def show_help(self,ctx,cmd:Optional[str]):
        self.show_hidden = False
        if cmd is None:
            menu = MenuPages(source = HelpMenu(ctx,list(self.bot.commands)),
                            delete_message_after = True,
                            timeout = 60.0)
            await menu.start(ctx)
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
