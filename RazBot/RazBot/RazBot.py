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
@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("pong")

@bot.command(pass_context=True)
async def leave(ctx):
    print("Disconnected")
    await bot.close()

@bot.command(pass_context=True)
async def joinV(ctx):
    cmd,chan = ctx.message.content.split(' ')
    channelToJoin = bot.get_channel(chan)
    print("Joined: " + channelToJoin.name)
    await bot.join_voice_channel(channelToJoin)

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

@bot.command(pass_context=True)
async def GetUser(ctx):
    text = ctx.message.content
    cmd,user = text.split(' ')
    print("Entered Name: " + user)
    member = ctx.message.mentions[0]
    print(member)

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

bot.run("NDAzNzM3OTQyNTUzNTI2Mjcz.DULqmA.M9aEeIvv34Mj7KvdU2aWMklwCtc")