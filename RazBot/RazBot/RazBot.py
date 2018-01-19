# imports
import discord
from discord.ext.commands import Bot
from discord.ext import commands

client = discord.Client()
bot_prefix = "!"
bot = commands.Bot(command_prefix=bot_prefix)

@bot.event
async def on_ready():
    print("Hello World")

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("pong")

@bot.command(pass_context=True)
async def leave(ctx):
    await bot.close()

@bot.command(pass_context=True)
async def joinV(ctx):
    channelToJoin = bot.get_channel('273826458928152577') # general channel
    print(channelToJoin.id)
    await bot.join_voice_channel(channelToJoin)

@bot.command(pass_context=True)
async def move(ctx):
    #toMove = bot.member
    text = ctx.message.content
    cmd,user,chan = text.split(' ')
    print(user)
    print(chan)
    #userInfo = bot.get_user_info(user)
    channel = bot.get_channel(chan)
    #print(userInfo.name)
    userInfo = ctx.message.mentions[0]#discord.utils.get(ctx.message.server.members, name=user)
    print(userInfo)
    await bot.move_member(userInfo, channel) # scrubs channel

@bot.command(pass_context=True)
async def GetUser(ctx):
    text = ctx.message.content
    cmd,user = text.split(' ')
    print("Entered Name: " + user)
    member = ctx.message.mentions[0]#discord.utils.get(ctx.server.members, name=user)
    print(member)

bot.run("NDAzNzM3OTQyNTUzNTI2Mjcz.DULqmA.M9aEeIvv34Mj7KvdU2aWMklwCtc")