# imports
import discord
import data
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
    sender = ctx.message.author
    if (sender.top_role.name == 'Manager'):
        print("Disconnected")
        await bot.close()

# !joinV + channelID tells bot to join a voice channel with that channelID
@bot.command(pass_context=True)
async def joinV(ctx):
    cmd,chan = ctx.message.content.split(' ')
    channelToJoin = bot.get_channel(chan)
    print("Joined: " + channelToJoin.name)
    await bot.join_voice_channel(channelToJoin)

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

# !NextRound shuffles users in voice channels based on the userData list in data.py, as well as the current round number (also found in data.py)
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
            mem = discord.utils.get(ctx.message.server.members, name=players[x])
            channel = bot.get_channel(data.dictTest[players[x]][data.roundNum])
            print("Moved: " + mem.name + " -> " + channel.name)
            await bot.move_member(mem, channel)

        data.roundNum += 1

# !MoveAll will move all users connected to any voice channel to be moved into the General voice channel
@bot.command(pass_context=True)
async def MoveAll(ctx):
    sender = ctx.message.author
    if (sender.top_role.name == 'Manager'):
        voiceList = list()
        voiceList.append(bot.get_channel(data.generalID))
        voiceList.append(bot.get_channel(data.standardAID))
        voiceList.append(bot.get_channel(data.standardBID))
        voiceList.append(bot.get_channel(data.standardCID))
        voiceList.append(bot.get_channel(data.standardDID))
        voiceList.append(bot.get_channel(data.doublesAID))
        voiceList.append(bot.get_channel(data.doublesBID))
        voiceList.append(bot.get_channel(data.doublesCID))
        voiceList.append(bot.get_channel(data.doublesDID))

        userList = list()
        for x in range(len(voiceList)):
            members = voiceList[x].voice_members
            for y in range(len(members)):
                userList.append(members[y])

        for m in userList:
            print("Moved: " + m.name + " -> General")
            channel = bot.get_channel(data.generalID)
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

token = input('Enter the Bot Token: ')
bot.run(token);