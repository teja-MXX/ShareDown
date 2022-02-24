import requests
import argparse
from sys import argv
from urllib.parse import unquote
import os
from time import time
import random
from colorama import Fore, Style
import platform

saveFolder = "/home/teja_mxx/Downloads/"

def ip_valid(IP):
    ipL = IP.split(".")
    if(len(ipL) != 4):
        print("Invalid IP Address Length")

def port_valid(port):
    port = int(port)
    if(port < 0 and port > 65535):
        print("PortRangeError : Port Address out of range")

# Formatting HTML file to get the files/folders names
def formatFiles(name):
    name = name[13:-9]
    nameLen = len(name) - 2
    nameLen = int(nameLen/2)
    name = name[:nameLen]
    return name

# Creating a Temporary Folder to Download all the files in it
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


def linuX(endPoint, banner):
    resp = requests.get(endPoint, allow_redirects=True)                       
    resp = resp.text.split("\n")                 
    resp = list(map(unquote, resp[10:-5]))                                #URL decoding using unquote
    resp = list(map(formatFiles,resp))
    for dir in resp:
        print(banner + Fore.GREEN + dir)
    
        if dir[-1] == "/":                                            
            dirr = dir
            if(len(dir.split(" ")) != 1):
                dirSplit = dir.split(" ")
                dirr = ""
                for x in range(0, len(dirSplit)-1 ,1):
                    dirr += dirSplit[x]+"\ "
                dirr += dirSplit[-1]
            
            endPointSplit = endPoint[len(serverURL):].split(" ")
            rendPoint= endPoint[len(serverURL):]
            if(len(endPointSplit) !=1):
                rendPoint = ""
                for xy in range(0, len(endPointSplit)-1 ,1):
                    rendPoint += endPointSplit[xy]+"\ "
                rendPoint += endPointSplit[-1]
            
            os.popen("mkdir "+saveFolder+"/"+rendPoint+dirr)
            r = linuX(endPoint+dir,banner[:-4]+"    |___")
            
        else:
            data = open(saveFolder+"/"+endPoint[len(serverURL):]+dir, "wb")
            fileData = requests.get(endPoint+dir, allow_redirects=True)
            data.write(fileData.content)
            data.close()
            #print(banner[:-4]+"    |___"+dir)
    return 1


def winDows(endPoint, banner):
    resp = requests.get(endPoint, allow_redirects=True)                       
    resp = resp.text.split("\n")                 
    resp = list(map(unquote, resp[10:-5]))                                #URL decoding using unquote
    resp = list(map(formatFiles,resp))

    
    for dir in resp:
        if(dir[-1] == "/"):
            os.popen("mkdir "+saveFolder+"/"+endPoint[len(serverURL):]+dir)
            r = winDows(endPoint+dir, banner[:-4]+"    |___")
        else:
            data = open(saveFolder+"/"+endPoint[len(serverURL):]+dir, "wb")
            fileData = requests.get(endPoint+dir, allow_redirects=True)
            data.write(fileData.content)
            data.close()
    
    return 1

parser = argparse.ArgumentParser()
sideBanner = "  |___ "
parser.add_argument("ip", help = "IP address of FTP Server", type=ip_valid)
parser.add_argument("port" , help = "FTP Server Port you want to access", type=port_valid)
args = parser.parse_args()
ip = argv[1]
port = argv[2]
serverURL = "http://"+ip+":"+port+"/"
saveFolder = fileCreate(saveFolder)
print(saveFolder)

if(platform.system() == "Linux"):
    linuX(serverURL, sideBanner)
else:
    winDows(serverURL, sideBanner)


#directoryTraverse(serverURL,sideBanner)
