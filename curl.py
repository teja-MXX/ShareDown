import requests
import argparse
from sys import argv
from urllib.parse import unquote
import os
from time import time
import random
from colorama import Fore, Style
import platform

#dst = "/home/teja_mxx/Downloads/"

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
def fileCreate(dst):
    random.seed(int(time()))
    text = ""
    for x in range(5):
        y = random.randrange(65,91)
        text += chr(y)
    dst += text
    os.popen("mkdir {}".format(dst))
    print("Temp Directory {} created to save files/folders".format(text))
    return dst


def linuX(endPoint, banner):
    resp = requests.get(endPoint, allow_redirects=True)                       
    resp = resp.text.split("\n")                 
    resp = list(map(unquote, resp[10:-5]))                                #URL decoding using unquote
    resp = list(map(formatFiles,resp))
    for webFile in resp:
        
        print(banner + Fore.GREEN + webFile)

        if webFile[-1] == "/":                                               # Checking if it's a directory                       
            # Linux format for creating file with Back Slashes
            DIR = webFile.replace("\'", "\\'")
            DIR = webFile.replace("$","\$")                                
            
            # If Name of the directory has spaces
            if(len(webFile.split(" ")) != 1):                                
                # If Name of the directory has Single and Double Quotes
                dirSplit = webFile.replace("\'", "\\'").split(" ")                                          
                DIR = ""
                for x in range(0, len(dirSplit)-1 ,1):
                    DIR += dirSplit[x]+"\ "
                DIR += dirSplit[-1]
    
            endPointSplit = endPoint[len(serverURL):].replace("\'", "\\'").split(" ")
            ENDPOINT= endPoint[len(serverURL):].replace("\'", "\\'")
            if(len(endPointSplit) !=1):
                ENDPOINT = ""
                for xy in range(0, len(endPointSplit)-1 ,1):
                    ENDPOINT += endPointSplit[xy]+"\ "
                ENDPOINT += endPointSplit[-1]
            ENDPOINT = ENDPOINT.replace("(","\(").replace(")","\)")
            DIR = DIR.replace("(","\(").replace(")","\)")
            os.popen("mkdir "+dst+"/"+ENDPOINT+DIR)
            r = linuX(endPoint+webFile,banner[:-4]+"    |___")
            
        else:
            print("DST - {} / endpoint - {} webFile - {}".format(dst, endPoint[len(serverURL):], webFile))
            data = open(dst+"/"+endPoint[len(serverURL):]+webFile, "wb")
            fileData = requests.get(endPoint+webFile, allow_redirects=True)
            data.write(fileData.content)
            data.close()
            
    return 1


def winDows(endPoint, banner):
    resp = requests.get(endPoint, allow_redirects=True)                       
    resp = resp.text.split("\n")                 
    resp = list(map(unquote, resp[10:-5]))                                #URL decoding using unquote
    resp = list(map(formatFiles,resp))

    
    for webFile in resp:
        if(webFile[-1] == "/"):
            os.popen("mkdir "+dst+"\\"+endPoint[len(serverURL):]+webFile)
            r = winDows(endPoint+webFile, banner[:-4]+"    |___")
        else:
            data = open(dst+"/"+endPoint[len(serverURL):]+webFile, "wb")
            fileData = requests.get(endPoint+webFile, allow_redirects=True)
            data.write(fileData.content)
            data.close()
    
    return 1

parser = argparse.ArgumentParser()
sideBanner = "  |___ "
parser.add_argument("ip", help = "IP address of FTP Server", type=ip_valid)
parser.add_argument("port" , help = "FTP Server Port you want to access", type=port_valid)
parser.add_argument("dst", help = "Destination URL to save your files")
args = parser.parse_args()
ip = argv[1]
port = argv[2]
dst = argv[3]+"/"
serverURL = "http://"+ip+":"+port+"/"

print("Destination Folder - {}".format(dst))

if(platform.system() == "Linux"):
    dst = argv[3]+"/"
    dst = fileCreate(dst)
    linuX(serverURL, sideBanner)
else:
    dst = argv[3]+"\\"
    dst = fileCreate(dst)
    winDows(serverURL, sideBanner)


#directoryTraverse(serverURL,sideBanner)
