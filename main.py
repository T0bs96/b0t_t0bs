import os
from os.path import join, dirname
from dotenv import load_dotenv
from discord.ext import commands
import server
from server import *
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

ver = "0.1.0"

#Load env vars
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
GATEWAY = os.environ.get("GATEWAY")
CONNECT = os.environ.get("CONNECT")

#Coding!  

class MyBot(commands.Bot):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

#Commands
bot = MyBot(command_prefix='$')

@bot.command()
async def version(ctx):
    await ctx.send("I am currently running version: " + ver)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def start(ctx):
    if server.Check(HOST):
        print("Server is turned on") 
        await ctx.send("Server is turned on")
        await ctx.send("connect " + CONNECT)
    else:
        if server.Start(GATEWAY, PORT):
            await ctx.send("Server is turning on...")
            while not server.Check(HOST):
                time.sleep(10)
                await ctx.send("Server is still turning on... Update in 10 seconds")
            if server.Check(HOST):
                await ctx.send("Server is running!")
                await ctx.send("connect " + CONNECT)
        else:
            print("Connection refused")
            await ctx.send("connection to server on " + PORT + "was refused!")

@bot.command()
async def stop(ctx):
    if server.ShutDown(HOST):
        await ctx.send("Server is shutting down in one minute")
    else:
        await ctx.send("Server was unable to shut down...")
        
client = bot
client.run(TOKEN)