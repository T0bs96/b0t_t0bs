#!/bin/python3
import paramiko
import telnetlib
import os
import time

from paramiko import AuthenticationException

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

def ShutDown(host):
    sshkey = paramiko.RSAKey.from_private_key_file("/home/tdp/.ssh/home_rsa")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username='tdp',pkey = sshkey)
        stdin, stdout, stderr = client.exec_command('sudo shutdown')
        return True
    except:
        return False