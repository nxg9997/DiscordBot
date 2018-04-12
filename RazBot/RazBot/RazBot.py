# imports
import discord
import data
import asyncio
import youtube_dl
from discord.ext.commands import Bot
from discord.ext import commands

'''
from appJar import gui
'''

client = discord.Client()
bot_prefix = "!"
bot = commands.Bot(command_prefix=bot_prefix)

# variables



# Start Up
@bot.event
async def on_ready():
    print("RazBot Connected")

# Commands

# !ping is used to check to see if the bot is active, bot will say "pong" in the chat
@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("pong")

# !leave will tell the bot to leave the server (logout)
@bot.command(pass_context=True)
async def leave(ctx):
    print("in leave")
    data.vc = None
    data.player = None
    if (ctx.message.author.id == '83713238620966912'):
        print("is nate")
        await bot.close()
    '''
    sender = ctx.message.author
    canUse = False;
    for r in ctx.message.author.roles:
        if r == 'BotMaster':
            canUse = True
    if (canUse):
        print("Disconnected")
        await bot.close()
        '''

# !joinV + channelID tells bot to join a voice channel with that channelID
@bot.command(pass_context=True)
async def joinV(ctx):
    # cmd,chan = ctx.message.content.split(' ')
    canUse = False;
    for r in ctx.message.author.roles:
        if r.name == 'BotMaster':
            canUse = True
    if (canUse):
        channelToJoin = bot.get_channel(ctx.message.author.voice_channel.id)
        print("Joined: " + channelToJoin.name)
        if (data.vc == None):
            data.vc = await bot.join_voice_channel(channelToJoin)
        else:
            await data.vc.move_to(channelToJoin)

# !joinV + channelID tells bot to join a voice channel with that channelID
@bot.command(pass_context=True)
async def joinVD(ctx):
    cmd,chan = ctx.message.content.split(' ')
    canUse = False;
    for r in ctx.message.author.roles:
        if r.name == 'BotMaster':
            canUse = True
    if (canUse):
        try:
            channelToJoin = bot.get_channel(chan)
            print("Joined: " + channelToJoin.name)
            if (data.vc == None):
                await bot.join_voice_channel(channelToJoin)
            else:
                await ctx.message.server.voice_client.move_to(channelToJoin)
        except Exception as e:
            print("already connected")

# !joinV + channelID tells bot to join a voice channel with that channelID
@bot.command(pass_context=True)
async def leaveV(ctx):
    canUse = False;
    for r in ctx.message.author.roles:
        if r.name == 'BotMaster':
            canUse = True
    if (canUse):
        try:
            await bot.voice_client_in(ctx.message.server).disconnect()
            data.vc = None
        except Exception as e:
            print("error in leaveV")

# !move + mention + channelID tells bot to move the mentioned user to a voice channel with the specified channelID
@bot.command(pass_context=True)
async def move(ctx):
    sender = ctx.message.author
    if (sender.top_role.name == 'Manager'):
        text = ctx.message.content
        cmd,user,chan = text.split(' ')
        # print(user)
        # print(chan)
        channel = bot.get_channel(chan)
        userInfo = ctx.message.mentions[0]
        # print(userInfo)
        print("Moved: " + userInfo.name + " -> " + channel.name)
        await bot.move_member(userInfo, channel)

# !GetUser prints the name of a mentioned user to the console (used for debug)
@bot.command(pass_context=True)
async def GetUser(ctx):
    text = ctx.message.content
    cmd,user = text.split(' ')
    print("Entered Name: " + user)
    member = ctx.message.mentions[0]
    print(member)

# !NextRound shuffles users in voice channels based on the userData list in data.py, as well as the current round number (also found in data.py) **OLD VERSION, DO NOT USE**
@bot.command(pass_context=True)
async def NextRoundv1(ctx):
    sender = ctx.message.author
    if (sender.top_role.name == 'Manager'):
        locRN = data.roundNum
        locRN += 1
        rNm = "" + str(locRN)
        print("Started Round: " + rNm)
        await bot.say("Started Round: " + rNm)
        channels = ["","","","","","","","","","","","","","","","","","",""]
        for x in range(len(data.userdata)):
            member,channels[0],channels[1],channels[2],channels[3],channels[4],channels[5],channels[6],channels[7],channels[8],channels[9],channels[10],channels[11],channels[12],channels[13] = data.userdata[x].split(',')
            # print(member)
            # print(channels[data.roundNum])
            mem = discord.utils.get(ctx.message.server.members, name=member)
            # print(mem)
            channel = bot.get_channel(channels[data.roundNum])
            print("Moved: " + member + " -> " + channel.name)
            await bot.move_member(mem, channel)
        
        data.roundNum += 1

# !NextRound will move players to the appropriate voice channels when called. Increments the round number each time
@bot.command(pass_context=True)
async def NextRound(ctx):
    sender = ctx.message.author
    if (sender.top_role.name == 'Manager' and data.roundNum < data.MAXROUNDS):
        locRN = data.roundNum;
        locRN += 1
        rNm = "" + str(locRN)
        print("Started Round: " + rNm)
        await bot.say("Started Round: " + rNm)
        players = list(data.userDataDict.keys())
        for x in range(len(players)):
            mem = discord.utils.get(ctx.message.server.members, name=players[x])
            channel = bot.get_channel(data.userDataDict[players[x]][data.roundNum])
            print("Moved: " + mem.name + " -> " + channel.name)
            await bot.move_member(mem, channel)

        data.roundNum += 1

# used to test the !NextRound command using test variables
@bot.command(pass_context=True)
async def TestRound(ctx):
    sender = ctx.message.author
    if (sender.top_role.name == 'Manager' and data.roundNum < data.MAXTEST):
        locRN = data.roundNum;
        locRN += 1
        rNm = "" + str(locRN)
        print("Started Round: " + rNm)
        await bot.say("Started Round: " + rNm)
        players = list(data.dictTest.keys())
        for x in range(len(players)):
            try:
                mem = discord.utils.get(ctx.message.server.members, name=players[x])
                channel = bot.get_channel(data.dictTest[players[x]][data.roundNum])
                print("Moved: " + mem.name + " -> " + channel.name)
                await bot.move_member(mem, channel)
            except:
                print("exception!")

        data.roundNum += 1

# !MoveAll will move all users connected to any voice channel to be moved into the General voice channel
@bot.command(pass_context=True)
async def MoveAll(ctx):
    sender = ctx.message.author
    if (sender.top_role.name == 'Manager'):
        print("manager!")
        voiceList = list()
        voiceList.append(bot.get_channel(data.g))
        voiceList.append(bot.get_channel(data.sA))
        voiceList.append(bot.get_channel(data.sB))
        voiceList.append(bot.get_channel(data.sC))
        voiceList.append(bot.get_channel(data.sD))
        voiceList.append(bot.get_channel(data.dA))
        voiceList.append(bot.get_channel(data.dB))
        voiceList.append(bot.get_channel(data.dC))
        voiceList.append(bot.get_channel(data.dD))

        userList = list()
        for x in range(len(voiceList)):
            members = voiceList[x].voice_members
            for y in range(len(members)):
                userList.append(members[y])

        for m in userList:
            print("Moved: " + m.name + " -> General")
            channel = bot.get_channel(data.g)
            await bot.move_member(m,channel)




# checks to see if the bot has elevated permissions (attempts to delete text channel)
@bot.command(pass_context=True)
async def TestPerm(ctx):
    bot.delete_channel('405489719074357248')

# !CheckUser will print the name of the sender if the sender is a Manager (used for debug)
@bot.command(pass_context=True)
async def CheckUser(ctx):
    sender = ctx.message.author
    if (sender.top_role.name == 'Manager'):
        print(sender.name)


@bot.command(pass_context=True)
async def PlayYT(ctx):
    canUse = False;
    for r in ctx.message.author.roles:
        if r.name == 'BotMaster':
            canUse = True
    if (canUse):
        if data.player != None:
            data.player.stop()
        msg = ctx.message.content
        cmd,url = ctx.message.content.split(' ')
        print(url)
        opts = {
                'default_search': 'auto',
                'quiet': True,
            }
        voice_channel = bot.get_channel(ctx.message.author.voice_channel.id)
    
       # data.vc = bot.voice_client_in(ctx.message.server)
        data.player = await data.vc.create_ytdl_player(url, ytdl_options=opts)
        data.player.volume = 0.25
        data.player.start()

@bot.command(pass_context=True)
async def StopYT(ctx):
    canUse = False;
    for r in ctx.message.author.roles:
        if r.name == 'BotMaster':
            canUse = True
    if (canUse):
        if data.player != None:
            data.player.stop()

@bot.command(pass_context=True)
async def FixBot(ctx):
    data.vc = bot.voice_client_in(ctx.message.server)
    data.vc.disconnect()
'''

@commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            await self.bot.say("Loading the song please be patient..")
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Enqueued ' + str(entry))
            await state.songs.put(entry)


@bot.event
async def on_message(message):
    sender = message.author
    if (sender.id != '403737942553526273'):
        if (sender.id == '160065743856074752'):
            await bot.send_message(message.channel, 'Memes')
            #await bot.say('Memes')

        # if (len(message.mentions) != 0):
           # await bot.send_message(message.channel, '<@%s>' % message.mentions[0].id)
           '''
'''
# mute all
@bot.command(pass_context=True)
async def MuteAll(ctx):
    sender = ctx.message.author
    if (sender.top_role.name == "Manager"):
        channel = bot.get_channel(data.pG)
        members = channel.voice_members
        print(len(members))
        for m in members:
            print("Muted: " + m.name)
            await bot.server_voice_state(m,mute=True)

# unmute all
@bot.command(pass_context=True)
async def UnmuteAll(ctx):
    sender = ctx.message.author
    if (sender.top_role.name == "Manager"):
        channel = bot.get_channel(data.pG)
        members = channel.voice_members
        for m in range(len(members)):
            print("Unmuted: " + members[m].name)
            await bot.server_voice_state(members[m],mute=False)
'''

'''
# functions for the gui buttons
def press(btnName):
    print(btnName)
    if (btnName == "Start"):
        token = app.getEntry("tokenEnt")
        bot.run(token);
    elif (btnName == "Leave"):
        exit()

def pressLeave(btnName):
    print(btnName)
    exit()

# creates gui
app = gui("RazBot")
# app.setIcon("razbotIcon.gif")
app.addLabel("tokenLab", "Bot Token:", 0, 0)
app.addEntry("tokenEnt", 0, 1)
app.addButtons(["Start", "Leave"], press, colspan=2)
# app.addButton("Leave", pressLeave, colspan=2)
app.go()
'''

token = input('Enter the Bot Token: ') # prompts user to enter the bot's api token
bot.run(token); # starts the bot