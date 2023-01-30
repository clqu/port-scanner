# Author: clqu
# Date: 2023-30-01
# Description: A simple port scanner written in python
# Version: 1.0.0
# License: MIT

# Importing the modules
import sys
import socket
from datetime import datetime
from pystyle import Colors, Write
from os import system, name
import threading

# Clear function for windows and linux
def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


# Clear the screen
clear()

tab = "        "

# I just installed python for this :P
Write.Print("""


        ▀███▀▀▀██▄                   ██       ▄█▀▀▀█▄█                                                     
         ██   ▀██▄                  ██      ▄██    ▀█                                                     
         ██   ▄██  ▄██▀██▄▀███▄█████████    ▀███▄    ▄██▀██ ▄█▀██▄ ▀████████▄ ▀████████▄   ▄▄█▀██▀███▄███ 
         ███████  ██▀   ▀██ ██▀ ▀▀  ██        ▀█████▄█▀  ████   ██   ██    ██   ██    ██  ▄█▀   ██ ██▀ ▀▀ 
         ██       ██     ██ ██      ██      ▄     ▀███      ▄█████   ██    ██   ██    ██  ██▀▀▀▀▀▀ ██     
         ██       ██▄   ▄██ ██      ██      ██     ███▄    ▄█   ██   ██    ██   ██    ██  ██▄    ▄ ██     
        ▄████▄     ▀█████▀▄████▄    ▀████   █▀█████▀ █████▀▀████▀██▄████  ████▄████  ████▄ ▀█████▀████▄   

                                               by @clqu
                                            version: 1.0.0


""", Colors.rainbow, interval=0, end=Colors.reset)


# Ask for a remote host to scan
inpuText = "$ Enter a remote host to scan: "
try:
    remoteServer = input(tab + inpuText)
    remoteServerIP = socket.gethostbyname(remoteServer)
except socket.gaierror:
    Write.Print(tab + "Hostname could not be resolved. Closing...\n", Colors.red)
    sys.exit()

# Ask for a port range
Range = input(tab + "$ Enter a port range to scan (e.g. 1-1000): ")
total = int(Range.split('-')[1]) - int(Range.split('-')[0])

# Ask for the number of threads
Threads = input(tab + "$ Enter the number of threads (e.g. 200): ")
if int(Threads) < 0:
    Write.Print(tab + "$ Too few threads, using {} threads".format(total), Colors.red)
    Threads = total



# Print a nice banner with information on which host we are about to scan
Write.Print("\n" + tab + "$ " + "-" * (len(inpuText) + len(remoteServerIP) + 1),
            Colors.cyan, interval=0)
Write.Print("""
        $ Remote Host: {}
        $ Remote IP: {}
        $ Range: {}
""".format(remoteServer, remoteServerIP, Range), Colors.cyan, interval=0)

Write.Print(tab + "$ " + "-" * (len(inpuText) + len(remoteServerIP) + 1),
            Colors.cyan, interval=0)


# Check what time the scan started
t1 = datetime.now()
Write.Print("\n" + tab + "$ Scanning started at: " + str(t1), Colors.cyan, interval=0)
Write.Print("\n" + tab + "$ Scanning {} ports...".format(total), Colors.cyan, interval=0)
Write.Print("\n" + tab + "$ Per port by thread: {}".format(int(total / int(Threads))), Colors.cyan, interval=0)
Write.Print("\n" + tab + "$ " + "-" * (len(inpuText) + len(remoteServerIP) + 1),
            Colors.cyan, interval=0)
Write.Print("\n", Colors.cyan, interval=0)

def thread_sleep():
    lock = threading.Lock()
    lock.acquire()
    lock.release()

# Using the range function to specify ports
def scan(port):
    s = socket.socket()
    s.settimeout(5)
    result = s.connect_ex((remoteServerIP, port))
    if result == 0:
        return {
            "port": port,
            "status": "open",
            "type": socket.getservbyport(port)
        }
    s.close()

# Thread Logger
def threadLogger(text):
    lock = threading.Lock()
    lock.acquire()
    print(tab + text)
    lock.release()

def startScan(start, end):
    try:
        thread_sleep()
        for port in range(start, end + 1):
            s = scan(port)
            if s != None:
                threadLogger("$ Port {}: {} - {}".format(s["port"], s["status"], s["type"]))

    except KeyboardInterrupt:
        Write.Print("\n" + tab + "$ You pressed Ctrl+C", Colors.red, interval=0)
        sys.exit()

    except socket.gaierror:
        Write.Print("\n" + tab + "$ Hostname could not be resolved. Closing...", Colors.red, interval=0)
        sys.exit()
    
    except socket.error:
        return

    
threads = []
for i in range(int(Threads)):
    start = int(Range.split('-')[0]) + (i * int(total / int(Threads)))
    end = start + int(total / int(Threads)) - 1
    t = threading.Thread(target=startScan, args=(start, end))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
    
# Scan ended
t2 = datetime.now()
total = t2 - t1
Write.Print("\n" + tab + "$ Scanning completed in: " + str(total), Colors.cyan, interval=0)
Write.Print("\n" + tab + "$ " + "-" * (len(inpuText) + len(remoteServerIP) + 1),
            Colors.cyan, interval=0)
Write.Print("\n", Colors.cyan, interval=0)