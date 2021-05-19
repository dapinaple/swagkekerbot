from datetime import datetime, timedelta
from random import randint
from typing import Optional

from discord import Embed, Member
from discord.ext.commands import CheckFailure, Cog, command, has_permissions, has_guild_permissions
from discord.ext.menus import ListPageSource, MenuPages

from ..db import db



class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=7)

    async def write_page(self, menu, offset, fields = []):
        len_data = len(self.entries)
        


        embed = Embed(title=f" {self.ctx.guild} Leaderboard",
                      colour=self.ctx.author.colour)
        embed.set_thumbnail(url=self.ctx.guild.icon_url)
        embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} members.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
            
        
        return embed

    async def format_page(self, menu, entries):
        
        offset = (menu.current_page*self.per_page) + 1

        fields = []
        table = ("\n".join(f"{idx+offset}. {self.ctx.guild.get_member(entry[0]).name} (XP: {entry[1]} | Level: {entry[2]})"
                for idx, entry in enumerate(entries)))

        fields.append(("Ranks", table))

        return await self.write_page(menu, offset, fields)







class Exp(Cog):
    def __init__(self, bot):
        self.bot = bot

        

    async def process_xp(self, message):
        xp, lvl, xplock = db.record("SELECT XP, lvl, XPLock FROM users WHERE UserID = ?", message.author.id)
        
        if datetime.utcnow() > datetime.fromisoformat(xplock):
            await self.add_xp(message, xp, lvl)
        
    async def add_xp(self, message, xp, lvl):
        xp_to_add = randint(10, 20)
        new_lvl = int(((xp+xp_to_add)//52) ** 0.55)

        db.execute("UPDATE users SET XP = XP + ?, lvl = ?, XPLock = ? WHERE UserID = ?",
                   xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=60)).isoformat(), message.author.id)
        
        if new_lvl > lvl:
            try:

                await self.levelup_channel.send(f"Kek! {message.author.mention} - you reached level **{new_lvl:,}**!")
            except:
                pass


    @command(name="level", brief = "gets the level of a member of a server")
    async def display_level(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        xp, lvl = db.record("SELECT XP, lvl FROM users WHERE UserID = ?", target.id) or (None, None)

        

        if lvl is not None:
            await ctx.send(f"**{target.display_name}** is on level **{lvl:,}** with **{xp:,}** XP.")

        else:
            await ctx.send("That member is not tracked by the experience system.")


    
    @command(name="rank",brief = "gets the rank of a user")
    async def display_rank(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        ids = db.column("SELECT UserID FROM users ORDER BY XP DESC")

        guildRank = [i for i in ids if self.bot.get_user(i) in ctx.guild.members]

        try:
            await ctx.send(f"**{target.display_name}** is rank **{guildRank.index(target.id)+1}** of **{len(guildRank)}**.")

        except ValueError:
            await ctx.send("I have no idea who that person is. ")

    @command(name = "setlevelchannel",brief = "sets the level up channel to the current channel")
    @has_guild_permissions(administrator = True)
    async def setlvlchannel(self,ctx):
        
        channel = ctx.channel.id

        db.execute('UPDATE guilds SET LevelChannel = ? WHERE GuildID = ?',channel,ctx.guild.id)
        db.commit()
        await ctx.send("Level up channel set!")

        

    @command(name="leaderboard", brief = "send the leaderboard for the server")
    async def display_leaderboard(self, ctx):
        records = []
        _records = db.records("SELECT UserID, XP, lvl FROM users ORDER BY XP DESC")
        for i in _records:

            if ctx.guild.get_member(i[0]):
                records.append(i)
        
        menu = MenuPages(source=HelpMenu(ctx, records),
                         clear_reactions_after=True,
                         timeout=60.0)
        await menu.start(ctx)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            
            
            self.bot.cogs_ready.ready_up("exp")





    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            

            _lvlch = db.field("SELECT LevelChannel FROM guilds WHERE GuildID = ?", message.guild.id)

            self.levelup_channel = self.bot.get_channel(_lvlch)

            if not self.levelup_channel:
                self.levelup_channel = message.channel
            
            await self.process_xp(message)
                


            


def setup(bot):
    bot.add_cog(Exp(bot))
