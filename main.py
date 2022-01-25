import os
from os.path import join, dirname
from dotenv import load_dotenv
from discord.ext import commands
import discord
import server
from server import *
import logging
import time
import datetime

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

ver = "0.3.4"

#Load env vars
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
GATEWAY = os.environ.get("GATEWAY")
CONNECT = os.environ.get("CONNECT")
PKEY = os.environ.get("PKEY")
UNAME = os.environ.get("UNAME")

#Set command prefix
prefix="sbot-"

#Coding! 

class MyBot(commands.Bot):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        game = discord.Game("Botting around")
        await client.change_presence(status=discord.Status.online, activity=game)

#Commands
bot = MyBot(command_prefix=prefix)

@bot.command()
async def version(ctx):
    await ctx.send("I am currently running version: " + ver)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.remove_command("help")
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Usable commands", description="This is a list of currently available commands", color=0xFF5733)
    embed.add_field(name=prefix + "help", value="Shows this list of commands", inline=False)
    embed.add_field(name=prefix + "ping", value="Test if bot is running", inline=False)
    embed.add_field(name=prefix + "start", value="Start T0bs' server", inline=False)
    embed.add_field(name=prefix + "stop", value="Stop T0bs' server", inline=False)
    embed.add_field(name=prefix + "status",value="Check server status", inline=False)
    embed.add_field(name=prefix + "version", value="See current version of the bot", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def status(ctx):
    message = await ctx.send("Checking system status...")
    embed = server.Status(HOST, prefix)
    await message.delete()
    await ctx.send(embed=embed) 


@bot.command()
async def start(ctx): 
    message = await ctx.send("Checking if server is on first...")
    if server.Check(HOST):
        await message.edit(content="Server is already turned on")
    else:
        await message.edit(content="Trying to turn on server...")
        if server.Start(GATEWAY, PORT):
            await message.edit(content="Server is turning on...")
            string="Server is still turning on"
            while not server.Check(HOST):
                string += '.'
                await message.edit(content=string)
            if server.Check(HOST):
                await message.delete()
                embed = server.Status(HOST, prefix)
                await ctx.send(embed=embed)
                await ctx.send("connect " + CONNECT)
        else:
            print("Connection refused")
            await message.edit(content="connection to server on " + PORT + "was refused!")

@bot.command()
async def stop(ctx):
    await ctx.send("Trying to gracefully shut down server...")
    if server.ShutDown(HOST, PKEY, UNAME):
        current_time = datetime.datetime.now()
        add = 1
        add_minutes = datetime.timedelta(minutes = add)
        _down_time = current_time + add_minutes
        down_time = _down_time.strftime("%H:%M:%S")
        message = await ctx.send(content="Server will shutdown at " + down_time)
        while server.Check(HOST):
            time.sleep(1)
        await message.edit(content="Server has been shut down")
    else:
        message = await ctx.send("Server was unable to shut down... If server is booting up, please wait until it has started.")

@bot.command()
async def test(ctx):
    await ctx.send("Testing something")
    i = 5
    message = await ctx.send("Message will be deleted in "+ str(i) +" seconds.")
    while i > 0:
        await message.edit(content="Message should be deleted in "+ str(i) +" seconds.")
        i = i - 1
        time.sleep(1)
        print (i)
    await message.delete()
client = bot
client.run(TOKEN)