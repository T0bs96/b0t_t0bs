import os
from os.path import join, dirname
from dotenv import load_dotenv
from discord.ext import commands
import discord
import server
from server import *
import logging
import time

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

ver = "0.3.0"

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
    await message.edit(embed=embed) 

@bot.command()
async def start(ctx): 
    message = await ctx.send("Checking if server is on first...")
    if server.Check(HOST):
        await message.edit(content="Server is already turned on")
    else:
        await message.edit(content="Trying to turn on server...")
        if server.Start(GATEWAY, PORT):
            await message.edit(content="Server is turning on...")
            i = 1
            while not server.Check(HOST):
                while i < 100:
                    time.sleep(1)
                    await message.edit(content="Server is still turning on..." + str(i) +" seconds has passed")
                    int(i)
                    i = i+1
            if server.Check(HOST):
                embed = server.Status(HOST)
                await message.edit(embed=embed)
                await ctx.send("connect " + CONNECT)
        else:
            print("Connection refused")
            await message.edit(content="connection to server on " + PORT + "was refused!")

@bot.command()
async def stop(ctx):
    message = await ctx.send("Trying to gracefully shut down server...")
    if server.ShutDown(HOST, PKEY, UNAME):
        i = 60
        await message.edit(content="Server is shutting down in " + str(i) + " seconds!")
        while server.Check(HOST):
            await message.edit(content="Server is shutting down in " + str(i) + " seconds!")
            int(i)
            i = i - 1
            time.sleep(1)
        await message.edit(content="Server has been shut down")
    else:
        await message.edit(content="Server was unable to shut down...")

@bot.command()
async def test(ctx):
    message = await ctx.send("Testing something...")
    embed = status(HOST)
    await message.edit(embed=embed)
client = bot
client.run(TOKEN)