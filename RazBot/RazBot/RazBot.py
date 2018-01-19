# imports
import discord
import data
from discord.ext.commands import Bot
from discord.ext import commands

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
async def NextRound(ctx):
    channels = ["",""]
    for x in range(len(data.userdata)):
        member,channels[0],channels[1] = data.userdata[x].split(',')
        # print(member)
        # print(channels[data.roundNum])
        mem = discord.utils.get(ctx.message.server.members, name=member)
        # print(mem)
        channel = bot.get_channel(channels[data.roundNum])
        print("Moved: " + member + " -> " + channel.name)
        await bot.move_member(mem, channel)
        
    data.roundNum += 1

@bot.command(pass_context=True)
async def MoveAll(ctx):
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

bot.run("NDAzNzM3OTQyNTUzNTI2Mjcz.DULqmA.M9aEeIvv34Mj7KvdU2aWMklwCtc")