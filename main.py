from email import message
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

ver = "0.2.0"

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

#Coding!  

class MyBot(commands.Bot):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        game = discord.Game("I am b0t!")
        await client.change_presence(status=discord.Status.idle, activity=game)

#Commands
bot = MyBot(command_prefix='$')

@bot.command()
async def version(ctx):
    await ctx.send("I am currently running version: " + ver)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def h(ctx):
    embed = discord.Embed(title="Usable commands", description="This is a list of currently available commands", color=0xFF5733)
    embed.add_field(name="$ping", value="Test if bot is running", inline=False)
    embed.add_field(name="$version", value="See current version of the bot", inline=False)
    embed.add_field(name="$start", value="Start T0bs' server", inline=False)
    embed.add_field(name="$stop", value="Stop T0bs' server", inline=False)
    embed.add_field(name="$status",value="Check server status (To be implemented in v. 0.3.0", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def start(ctx): 
    if server.Check(HOST):
        await ctx.send("Server is turned on")
    else:
        message = await ctx.send("Trying to turn on server...")
        if server.Start(GATEWAY, PORT):
            await message.edit(content="Server is turning on...")
            i = 1
            while not server.Check(HOST):
                time.sleep(10)
                await message.edit(content="Server is still turning on..." "["+ str(i) +"] retrie(s)")
                int(i)
                i = i+1
            if server.Check(HOST):
                await message.edit(content="Server is *running!*")
                await ctx.send("connect " + CONNECT)
        else:
            print("Connection refused")
            await message.edit(content="connection to server on " + PORT + "was refused!")

@bot.command()
async def stop(ctx):
    message = await ctx.send("Trying to shutdown server...")
    if server.ShutDown(HOST, PKEY, UNAME):
        await message.edit(content="Server is shutting down in one minute")
        time.sleep(60)
        if server.Check(HOST):
            await message.edit(content="Server is shutting down in one minute")
    else:
        await message.edit(content="Server was unable to shut down...")
        
client = bot
client.run(TOKEN)