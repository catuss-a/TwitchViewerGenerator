#!/usr/bin/python

import re
import requests
import subprocess
import json
import sys
import threading
import time
from Queue import Queue

numberOfViewers = int(sys.argv[1])
streamUrl = sys.argv[2]
startTime = time.time()
numberOfSockets = 0
concurrent = 25
q=Queue(concurrent*2)
pattern = "((?P<login>\w+):(?P<password>\w+)@)?(?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(:(?P<port>\d+))?"

dictProxy = [
]

def getURL(): # Get tokens
    global streamUrl

    while True:
        output = subprocess.Popen(["livestreamer", streamUrl, "-j"], stdout=subprocess.PIPE).communicate()[0]
        l = json.loads(output)
        if 'streams' in l and 'worst' in l['streams'] and 'url' in l['streams']['worst']:
            return l['streams']['worst']['url'] # Parse json and return the URL parameter

def view(): # Opens connections to send views
    global numberOfSockets
    global q
    global dictProxy

    url = []
    prox = { "http": ""}
    if len(dictProxy) < 1:
        print 'error no proxy left'
        return
    prox["http"] = "http://" + dictProxy[0]["ip"] + ":80"
    dictProxy.pop(0)

    print 'Proxy: ' + str(prox["http"])
    print 'getting an URL...'
    for i in range(10):
        link = getURL()
        print 'URL gotten: ' + link
        url.append(link)
    while True:
        print 'sup'
        for link in url:
            print 'get THQT ' + link + ' ' + prox['http']
            requests.head(link, proxies=prox)

if __name__ == '__main__':

    nb_proxy=0
    fd = open('proxies', 'r')
    line = fd.readline()
    while line:
        m = re.search(pattern, line)
        if m:
            nb_proxy += 1
            dictProxy.append({ "ip": m.group(0) , "cpt": 0})
        line = fd.readline()

    print "number of proxies: " + str(nb_proxy)
    for i in range(numberOfViewers / 10):
        try:
            t=threading.Thread(target=view)
            t.daemon=True
            t.start()
        except:
            print 'thread error'
        time.sleep(1)
        print '10 more viewers...'

    while True:
        time.sleep(10)
