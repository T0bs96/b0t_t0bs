#!/bin/python3
import paramiko
import discord
import socket
from wakeonlan import send_magic_packet

def Start(MAC):
    try:
        send_magic_packet(MAC)
        return True
    except:
        return False

def Check(host):
    port = 22
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    if result == 0:
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
def Status(host, prefix):
    if Check(host):
        state = "RUNNING!"
        embed = discord.Embed(title="Status:", description="Following services and their status", color=0x00a86b)
        embed.add_field(name="Server status", value=state, inline=True)
    else:
        state = "DOWN :("
        embed = discord.Embed(title="Status:", description="Following services and their status", color=0xFF5733)
        embed.add_field(name="Server status", value=state + "\nUse **" + prefix + "start** to start the server", inline=True)
    return embed

def TestStart(MAC):
    try:
        send_magic_packet(MAC)
        return True
    except:
        return False