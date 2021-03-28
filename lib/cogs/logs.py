import asyncio
from datetime import datetime

import pytz
from discord import Color, Embed, Member, channel, guild
from discord.ext.commands import Cog, command

from random import randint
class Logs(Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.logChannel = self.bot.get_channel(800636861793304606)
            self.listOfClipees =  [673403025410359337]    
            self.estelogs = self.bot.get_channel(809099936720617548)
            self.ghostLogs = self.bot.get_channel(821518416158261268)
            print(f"ghost logs is {self.ghostLogs}")
            self.bot.cogs_ready.ready_up("log")     
            self.estebanlol = await self.bot.fetch_user(673403025410359337)

    @Cog.listener()
    async def on_message(self,message):
        
        #nobody disses my bot

        forbiddenWords = ["nigger","nigga","niggers","niggas"]
        for word in message.content.split():
            if message.content.lower() == "fuck you poopshitter":
                await message.channel.send('***Ah nigga don\'t hate me cause I\'m beautiful nigga. Maybe if you got rid of that old yee yee ass haircut, you\'d get some bitches on yo dick.Oh, better yet, maybe Tanisha\'ll call your dog ass if she stops fuckin\' with that brain surgeon or lawyer she fucking with. Niiggaaa***')
                                                
                break
        if message.author.id in self.listOfClipees:
            if message.content.startswith("https") or message.content.startswith("cdn") or len(message.attachments) != 0 and message.channel.id != 784152789042593832:
                for attachment in message.attachments:
                    await self.estelogs.send(f"{message.author} sent this: {attachment.url} in {message.channel.mention} in the server **{message.guild}**")
                if message.content.startswith("https") or message.content.startswith("cdn"):
                    await self.estelogs.send(f"{message.author} sent this {message.content} in {message.channel.mention} in the server **{message.guild}**")
        
        if isinstance(message.channel, channel.DMChannel) and message.author != self.bot.user:
            await message.channel.send("https://tenor.com/view/dono-wall-talking-wall-bricks-gif-17741481")
            # elif word.lower() in forbiddenWords:
            #     await message.author.send("nword bad")
            #     print(f"send nword response to {message.author.name}")  

        # await self.bot.process_commands(message
        if message.author.id ==673403025410359337:
            pass
            # await message.delete(delay = randint(1,5))        
    @Cog.listener()
    async def on_member_join(self,member):
        guild = member.guild
        try:
            

            await guild.system_channel.send(f"Hello {member.mention} and welcome to **{guild}**! Enjoy your stay!")

        except:
            for channel in guild.channels:
                try:
                    await channel.send(f"Hello {member.mention} and welcome to **{guild}**! Hope you enjoy your stay!")
                    break
                except:
                    continue

        
    @Cog.listener()
    async def on_message_delete(self,message):
        if not message.author.bot:
           
            if (len(message.mentions) > 0 or len(message.role_mentions)> 0 or message.mention_everyone == True) and message.guild.id == 821513106403360809 :

                embed = Embed(title = 'Ghost Ping Found!',description = '', color = Color.dark_blue())
                embed.add_field(name = "User:",value = message.author,inline = True)
                embed.add_field(name = "Message:",value = f"{message.content} ",inline = True)
                embed.set_thumbnail(url = message.author.avatar_url)
                
                d = datetime.now()
                timezone = pytz.timezone("America/New_York")
                d_aware = timezone.localize(d)
                
                embed.timestamp = d_aware
                
                await self.ghostLogs.send(embed = embed)
            
            #clipping ppl i.e. estebanlol
            if message.author.id in self.listOfClipees and not message.content.startswith("https") : 
                embed =Embed(title = '',description = f'**{message.author.mention} sent a message in {message.channel.mention} in {message.guild}**\n {message.content}',color = Color.dark_blue())
                embed.set_author(name = message.author,icon_url = message.author.avatar_url)
                    
                await self.estelogs.send(embed=embed)

def setup(bot):
    bot.add_cog(Logs(bot))
