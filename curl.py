import requests
import argparse
from sys import argv
from urllib.parse import unquote
import os
from time import time
import random
from colorama import Fore, Style

saveFolder = "/home/teja_mxx/Downloads/"

def ip_valid(IP):
    ipL = IP.split(".")
    if(len(ipL) != 4):
        print("Invalid IP Address Length")

def port_valid(port):
    port = int(port)
    if(port < 0 and port > 65535):
        print("PortRangeError : Port Address out of range")

def formatFiles(name):
    name = name[13:-9]
    nameLen = len(name) - 2
    nameLen = int(nameLen/2)
    name = name[:nameLen]
    return name

def fileCreate(saveFolder):
    random.seed(int(time()))
    text = ""
    for x in range(5):
        y = random.randrange(65,91)
        text += chr(y)
    saveFolder += text
    os.popen("mkdir {}".format(saveFolder))
    print("Temp Directory {} created to save files/folders".format(text))
    return saveFolder


def directoryTraverse(endPoint, banner):
    resp = requests.get(endPoint, allow_redirects=True)
    resp = resp.text.split("\n")
    resp = list(map(unquote, resp[10:-5]))
    resp = list(map(formatFiles,resp))
    for dir in resp:
        
        if dir[-1] == "/":
            print(banner + Fore.GREEN + dir)
            r = directoryTraverse(endPoint+dir,banner[:-4]+"    |___")
            
        else:
            print(banner+dir)
            #print(banner[:-4]+"    |___"+dir)
    return 1


parser = argparse.ArgumentParser()
sideBanner = "  |___ "
parser.add_argument("ip", help = "IP address of FTP Server", type=ip_valid)
parser.add_argument("port" , help = "FTP Server Port you want to access", type=port_valid)
args = parser.parse_args()
ip = argv[1]
port = argv[2]
server = "http://"+ip+":"+port+"/"
saveFolder = fileCreate(saveFolder)
print(saveFolder)
print("\n ["+server+"]")
directoryTraverse(server, sideBanner)
