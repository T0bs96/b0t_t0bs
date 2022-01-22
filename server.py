#!/bin/python3
import paramiko
import telnetlib
import os
import discord

def Start(gateway,port):
    try:
        telnetlib.Telnet(gateway, port, 2)
        return True
    except:
        return False

def Check(host):
    response = os.system("ping -c 1" + " " + host)

    if response == 0:
        return True
    else:
        return False

def ShutDown(host, pkeyPath, uname):
    sshkey = paramiko.RSAKey.from_private_key_file(pkeyPath)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username = uname, pkey = sshkey)
        stdin, stdout, stderr = client.exec_command('sudo shutdown')
        client.close()
        return True
    except:
        return False
def Status(host):
    if Check(host):
        state = "RUNNING!"
        embed = discord.Embed(title="Status:", description="Following services and their status", color=0x00a86b)
        embed.add_field(name="Server status", value=state, inline=True)
    else:
        state = "DOWN :("
        embed = discord.Embed(title="Status:", description="Following services and their status", color=0xFF5733)
        embed.add_field(name="Server status", value=state + "\nUse $start to start the server", inline=True)
    return embed