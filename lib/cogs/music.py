import asyncio
import datetime as dt
import re
import typing as t
from enum import Enum

import discord
import wavelink
from discord.ext.commands import (ChannelNotFound, Cog, CommandError, Context,
                                  MissingPermissions, command, has_any_role,
                                  has_role)
from lyricsgenius import Genius

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
LYRICS_URL = "https://some-random-api.ml/lyrics?title="
HZ_BANDS = (20, 40, 63, 100, 150, 250, 400, 450, 630, 1000, 1600, 2500, 4000, 10000, 16000)
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


class AlreadyConnectedToChannel(CommandError):
    pass

class NoVoiceChannel(CommandError):
    pass

class QueueIsEmpty(CommandError):
    pass

class UserNotInVoice(CommandError):
    pass

class NoTracksFound(CommandError):
    pass

class PlayerIsAlreadyPaused(CommandError):
    pass

class NoMoreTracks(CommandError):
    pass

class NoPreviousTrack(CommandError):
    pass

class InvalidRepeatMode(CommandError):
    pass

class NoLyricsFound(CommandError):
    pass

class InvalidTimeString(CommandError):
    pass

class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE


    @property
    def is_empty(self):
        return not self._queue

    def add(self,*args):
        self._queue.extend(args)

    @property
    def first_track(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[0]

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]
        

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty
        return self._queue[self.position+1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty
        return self._queue[:self.position]
    
    @property
    def length(self):
        return len(self._queue)


    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]
    
    def empty(self):
        self._queue.clear()
        self.position = 0
    def remove_song(self, index):
        del self._queue[index]

    def set_repeat_mode(self,mode):
        if mode == "none":
            self.repeat_mode =RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    
        






class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.eq_levels = [0.] * 15
        self.ctx = None
        



    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self,ctx,tracks):
        if not tracks:
            raise NoTracksFound
        
        
        
        if isinstance(tracks,wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)

        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            
            
            embed = discord.Embed(
                description = f"Queued [{tracks[0].title}](http://youtube.com/watch?v={tracks[0].ytid}) [{ctx.author.mention}]",
                color = ctx.author.color
            )
            if self.queue.current_track == tracks[0]:
                embed.title = "Now Playing"
                embed.description = embed.description.strip("Queued ")
        
            
            await ctx.send(embed= embed)
        else:
            if (track := await self.choose_track(ctx,tracks)) is not None:
                self.queue.add(track)
                embed = discord.Embed(
                    
                description = f"Queued [{track.title}](http://youtube.com/watch?v={track.ytid}) [{ctx.author.mention}]",
                color = ctx.author.color
            )
                if self.queue.current_track == tracks[0]:
                    embed.title = "Now Playing"
                    embed.description = embed.description.strip("Queued ")
                       
            
                msg = await self.ctx.send(embed = embed)
                
                
                
        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()
        
            

    async def choose_track(self,ctx,tracks):
        def _check(r,u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )
        embed = discord.Embed(
            title = "Choose a Track",
            description = (
                "\n".join(
                    f"**{i+1}** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i,t in enumerate(tracks[:5])
                )
            ),
            color = ctx.author.color,
            timestamp = dt.datetime.utcnow()
        )
        embed.set_author(name = "Search Results")
        embed.set_footer(text = f"Request by {ctx.author.display_name}",icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed = embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks),len(OPTIONS))]:
            await msg.add_reaction(emoji)
        
        try:
            reaction, _= await self.bot.wait_for("reaction_add",timeout=60,check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]


    # # # # # # PLAYING COMMANDS
    async def start_playback(self):
        await self.play(self.queue.current_track)
        

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
                
                embed = discord.Embed(    
                title = "Now Playing",
                description = f"[{track.title}](http://youtube.com/watch?v={track.ytid}) [{self.ctx.author.mention}]",
                color = self.ctx.author.color
            )
                # if self.queue.current_track == track:
                #     embed.title = "Now Playing"
                #     embed.description.strip("Queued ")
                       
            
                msg = await self.ctx.send(embed = embed)
                
            
                
        except QueueIsEmpty:
            pass
    async def repeat_track(self):
        
        await self.play(self.queue.current_track)
                
        embed = discord.Embed(  
        title = "Now Playing", 
        description = f"[{self.queue.current_track.title}](http://youtube.com/watch?v={self.queue.current_track.ytid}) [{self.ctx.author.mention}]",
        color = self.ctx.author.color
        )
        
                    
        
        msg = await self.ctx.send(embed = embed)
            
    
        

    







class Music(Cog, wavelink.WavelinkMixin):
    def __init__(self,bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot = bot)
        self.bot.loop.create_task(self.start_nodes())

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f"Wavelink node '{node.identifier}' ready.")


    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self,node,payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    

    async def cog_check(self,ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Srry i can't play music here")
            return False
        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2444,
                "rest_uri": "http://127.0.0.1:2444",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "europe",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)

        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @command(name="connect", aliases=["join"],brief = "connects bot to current voice channel")
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.send(f"Connected to {channel.name}.")

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send("Already connected to a voice channel")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("What channel?")


     
    @command(name = "disconnect",aliases =["leave"],brief = "disconnect the bot from a channel")
    @has_any_role("dj","DJ","Dj") #change to make it guild specific with db
    async def disconnect_command(self,ctx):
        
        player = self.get_player(ctx)
        if ctx.author.voice:
            await player.teardown() 
        else:
            raise UserNotInVoice

    @disconnect_command.error
    async def disconnect_command_error(self,ctx,exc):
        if isinstance(exc,UserNotInVoice):
            await ctx.send("You have to be in a vc to use that")

      
    @command(name = "play",brief = "plays a track given a name or url")
    @has_any_role("dj","DJ","Dj") 
    async def play_command(self,ctx, *, query:t.Optional[str]):
        player = self.get_player(ctx)
        

        await player.connect(ctx) if not player.is_connected else None

        if not ctx.author.voice:
            raise UserNotInVoice
        else:
            player.ctx = ctx

        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty
           

            await player.set_pause(False)
            await ctx.send("Track Resumed")
        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error 
    async def play_command_error(self,ctx,exc):
        if isinstance(exc,UserNotInVoice):
            await ctx.send("You have to be in a channel to use that")
        elif isinstance(exc,QueueIsEmpty):
            await ctx.send("There's nothing to play")
            
    
    @command(name = "queue",brief = "send the current queue")
    async def queue_command(self,ctx,*,show: t.Optional[int] = 10):
        player = self.get_player(ctx)
        if player.queue.is_empty:
            raise QueueIsEmpty
        
        embed = discord.Embed(
            title = "Queue",
            color = ctx.author.color,
            timestamp = dt.datetime.utcnow()

        )
        embed.set_footer(text = f"Request by {ctx.author.display_name}",icon_url=ctx.author.avatar_url)
        embed.add_field(name="Currently Playing",value = getattr(player.queue.current_track,"title","No Tracks Playing"),inline = False)
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name = "Next Track",
                value = "\n".join(f"{i+1}) **{t.title}**" for i,t in enumerate(player.queue.upcoming[:show])),
                inline =False
            )
        await ctx.send(embed=embed)
        


    @queue_command.error 
    async def queue_command_error(self,ctx,exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is empty")

    
    @command(name = "pause",brief ="take a wild guess (pauses the current track)")
    @has_any_role("dj","DJ","Dj")
    async def pause_command(self,ctx):
        player = self.get_player(ctx)
        if player.is_paused:
            raise PlayerIsAlreadyPaused
        await player.set_pause(True)
        await ctx.send("Playback paused")

    @pause_command.error 
    async def pause_command_error(self,ctx,exc):
        if isinstance(exc,PlayerIsAlreadyPaused):
            await ctx.send("Playback is already paused")
    
    
    @command(name = "stop",brief = "absolutely obliterates the queue and player (not rly just resets the queue)")
    @has_any_role("dj","DJ","Dj")
    async def stop_command(self,ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.send("Playback stopped")

    @command(name ="skip",aliases = ["next"],brief = "goes to the next track in the queues")
    @has_any_role("dj","DJ","Dj")
    async def skip_command(self,ctx):
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks
        
        await player.stop()
        

    @skip_command.error
    async def skip_command_error(self,ctx,exc):
        if isinstance(exc, NoMoreTracks):
            await ctx.send("There are no more songs")
        elif isinstance(exc,QueueIsEmpty):
            await ctx.send("Could not skip bc queue is empty")
    
    @command(name ="back",aliases = ["previous","prev"],brief = "goes back one track in the queue")
    @has_any_role("dj","DJ","Dj")
    async def back_command(self,ctx):
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTrack
        
        player.queue.position -= 2

        await player.stop()
        

    @back_command.error
    async def back_command_error(self,ctx,exc):
        if isinstance(exc, NoPreviousTrack):
            await ctx.send("There are no previous tracks")
        elif isinstance(exc,QueueIsEmpty):
            await ctx.send("Could not go back because the queue is empty")

    @command(name = "repeat",aliases = ["replay"],brief = "sets the queue to either 1:repeat current song, all: repeat all songs in queue, none: repeat no songs")
    @has_any_role("dj","DJ","Dj")
    async def repeat_command(self,ctx,mode:str):
        if mode not in ("none","1","all"):
            raise InvalidRepeatMode
        
        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        await ctx.send(f"Repeat mode has been set to {mode}")

    @repeat_command.error 
    async def repeat_command_error(self,ctx,exc):
        if isinstance(exc,InvalidRepeatMode):
            await ctx.send("Invalid repeat mode: choose all, 1, or none")
            
    @command(name ="lyrics",brief = "Gets the lyrics of what is currently playing (scuffed), or the lyrics of a query (not as scuffed)")
    async def lyrics_command(self,ctx,*,name :t.Optional[str]):
        player = self.get_player(ctx)
        name = name or player.queue.current_track.title
        
        print(name)
        
        
        genius = Genius("5NJogQfjclEsm09U859rLrmK6CI0irVwM2a25zMRsyIJImdxsinZ-r55Z22Kncwc")
        song = genius.search_song(title = name)
        
        
        if len(song.lyrics) > 5000:
            return await ctx.send(f"<{song.url}>")
        
        embed = discord.Embed(
            title = song.title,
            description = song.lyrics,
            color = ctx.author.color,
            timestamp = dt.datetime.utcnow()
        )
        embed.set_thumbnail(url = song.song_art_image_url)
        embed.set_author(name=song.artist)
        
        msg = await ctx.send(embed = embed)  
        await asyncio.sleep(120) 
        await msg.delete()
    @lyrics_command.error
    async def lyrics_command_error(self,ctx,exc):
        if isinstance(exc,AttributeError):
            await ctx.send("No lyrics found")
            
    @command(name="playing", aliases=["np"],brief="gives some info about the track playing")
    async def playing_command(self, ctx):
        player = self.get_player(ctx)

        if not player.is_playing:
            raise PlayerIsAlreadyPaused

        embed = discord.Embed(
            title="Now playing",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow(),
        )
        embed.set_author(name="Playback Information")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Track title", value=player.queue.current_track.title, inline=False)
        embed.add_field(name="Artist", value=player.queue.current_track.author, inline=False)

        position = divmod(player.position, 60000)
        length = divmod(player.queue.current_track.length, 60000)
        embed.add_field(
            name="Position",
            value=f"{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}",
            inline=False
        )

        await ctx.send(embed=embed)

    @playing_command.error
    async def playing_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("There is no track currently playing.")
    
    @command(name ="skipto",brief = "skips to a track in the queue given an index")
    @has_any_role("dj","DJ","Dj")
    async def skipto_command(self,ctx,index: int):
        player = self.get_player(ctx)
        
        if player.queue.is_empty:
            raise QueueIsEmpty
        
        if not 0 <= index <= player.queue.length:
            raise NoMoreTracks
        
        player.queue.position = index - 1
        await player.stop()
    
    @skipto_command.error
    async def skipto_command_error(self,ctx,exc):
        if isinstance(exc,QueueIsEmpty):
            await ctx.send("There is nothing in the queue")
        elif isinstance(exc,NoMoreTracks):
            await ctx.send("There are no more tracks")
        
    
    @command(name="restart",brief = "replays the current track")
    @has_any_role("dj","DJ","Dj")
    async def restart_command(self, ctx):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        await player.seek(0)
        await ctx.send("Track restarted.")

    @restart_command.error
    async def restart_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("There are no tracks in the queue.")
            
                               
    @command(name="seek",brief = "goes to a specific part of the track [format min:sec]")
    @has_any_role("dj","DJ","Dj")
    async def seek_command(self, ctx, position: str):
        player = self.get_player(ctx)           
                
        if not (match := re.match(TIME_REGEX,position)):
            raise InvalidTimeString
        
        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        await ctx.send("Seeked.")
    
    @command(name="removesong",brief = "removes a track from the queue given an index")
    @has_any_role("dj","DJ","Dj")
    async def removesong_command(self, ctx,index: int):
        player = self.get_player(ctx)
        
        if not 0 <= index <= player.queue.length:
            raise NoMoreTracks
        
        player.queue.remove_song(index-1)
        
        
        



def setup(bot):
    bot.add_cog(Music(bot)) 
