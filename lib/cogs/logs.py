from discord import Member, guild
from discord.ext import commands
from discord.ext.commands import BucketType, CommandOnCooldown, cooldown
from discord.permissions import Permissions
from discord.utils import get
from discord.voice_client import VoiceClient
from discord import channel
import asyncio


class Logs(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.listOfClipees =  [673403025410359337,]    
                

    @listener()
    async def on_message(self,message):
        logs = client.get_channel(809099936720617548)
        
        #nobody disses my bot

        forbiddenWords = ["nigger","nigga","niggers","niggas"]
        for word in message.content.split():
            if message.content.lower() == "fuck you poopshitter":
                await message.channel.send('''***Ah nigga don't hate me cause I'm beautiful nigga. Maybe if you got rid of that old yee yee ass haircut, you'd get some bitches on yo dick.
                                                Oh, better yet, maybe Tanisha'll call your dog ass if she stops fuckin' with that brain surgeon or lawyer she fucking with. Niiggaaa***''')
                print("this came from logs cog")
                break
        if message.author.id in listOfClipees:
            if message.content.startswith("https") or message.content.startswith("cdn") or len(message.attachments) != 0 and message.channel.id != 784152789042593832:
                for attachment in message.attachments:
                    await logs.send(f"{message.author} sent this: {attachment.url} in {message.channel.mention} in the server **{message.guild}**")
                if message.content.startswith("https") or message.content.startswith("cdn"):
                    await logs.send(f"{message.author} sent this {message.content} in {message.channel.mention} in the server **{message.guild}**")
            
        if isinstance(message.channel, channel.DMChannel) and message.author != client.user:
            await message.channel.send("https://tenor.com/view/dono-wall-talking-wall-bricks-gif-17741481")
            # elif word.lower() in forbiddenWords:
            #     await message.author.send("nword bad")
            #     print(f"send nword response to {message.author.name}")  

        await client.process_commands(message)