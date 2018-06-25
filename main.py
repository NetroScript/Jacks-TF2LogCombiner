# -*- coding: utf-8 -*-
from io import BytesIO, StringIO
import zipfile
import urllib.request as urllib2
import codecs
import requests
import time
import datetime
import webbrowser
import json
import os.path
from collections import OrderedDict
from distutils.version import LooseVersion


def get_important(log, experimental):
    startline = 0
    endline = 0
    lc = 0
    tournament = False
    knownnames = []
    out = ""

    tournamentexists = True

    if "Tournament mode started" not in "".join(log):
        tournamentexists = False

    for line in log:
        if lc == 0:
            out = line+"\n"
        t = line.split(": ")
        if len(t) > 1:
            tcl = t[1]
            if tcl.startswith("Tournament mode started"):
                tournament = True
            if tcl.startswith('World triggered "Round_Start"') and (not tournament) and tournamentexists:
                startline = lc
                tournamentexists = False
            elif tcl.startswith("Log file closed."):
                endline = lc

        lc += 1

    if endline == 0:
        endline = lc-1


    # minimize the log a tiny bit
    if experimental:
        lc = len(log)-1
        for line in reversed(log):
            t = line.split(": ")
            if len(t) > 1:
                tcl = t[1]
                if tcl[0] == '"':
                    eventname = tcl[1:].split("><")[0]
                    for n in knownnames:
                        if lc+1000 < endline:
                            log[lc] = log[lc].replace(n, n[:1]+"<"+"".join(n.split("<")[-1:]))
                    if len(eventname) > 0:
                        if eventname+">" not in knownnames:
                            knownnames.append(eventname+">")
            lc -= 1

    for line in log[startline:endline]:
        if not experimental or not ('triggered "shot_hit"' in line or 'triggered "shot_fired"' in line):
            out += line

    return out


def getlog(url):
    logid = urllib2.urlparse(url).path.split("/")[1]
    myzipfile = zipfile.ZipFile(BytesIO(urllib2.urlopen("http://logs.tf/logs/log_"+logid+".log.zip").read()), "r")
    out = []
    for name in myzipfile.namelist():
        with myzipfile.open(name, "r") as readfile:
            for line in codecs.iterdecode(readfile, 'utf8', errors='ignore'):
                out.append(line)
    return out


def getmap(url):
    return urllib2.urlopen(url).read().decode('utf-8').split('<h3 id="log-map">')[1].split("</h3>")[0]


def loadsettings():
    i = 0
    with open("settings") as f:
        ro = f.read().split("\n")
    for t in op:
        options[t] = ro[i]
        i += 1
        

def optmenu(question, list):
    maxv = len(list)
    accepted = False
    while not accepted:
        cur = 1
        print(question)
        for opt in list:
            print("   " + str(cur) + ")   - " + opt)
            cur+=1
        a = input()
        if a.isdigit():
            a = int(a)
            if a > 0 and a <= maxv:
                return a-1
            else:
                print("Your choice is outside the range")
        else:
            print("Please input a number")

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def timesort(log):
    times = log[2:23]
    return time.mktime(datetime.datetime.strptime(times, "%m/%d/%Y - %H:%M:%S").timetuple())


def interface():
    appending = True
    logs = []
    maps = []
    ids = []
    wholesize = 0
    outlog = ""
    a = optmenu("Do you want to use experimental mode for further minifying? (Expect bugs)", ["No", "Yes"])
    if a == 1:
        experimental = True
    else:
        experimental = False
    while(appending):
        print("Paste the log you want to upload:")
        tmplog = input()
        u = urllib2.urlparse(tmplog)
        cont = False
        if (u.netloc == "www.logs.tf" or u.netloc == "logs.tf") and u.path.split("/")[1].isdigit():
            clog = get_important(getlog(tmplog), experimental)
            print("Size of this log: "+sizeof_fmt(len(clog.encode('utf-8'))))
            if(wholesize + len(clog.encode('utf-8')) > 5 * 1000 * 1000):
                a = optmenu("File would be bigger than 5 MB - But it seems the API doesn't enforce it, so feel free to continue.", ["Continue", "Abort", "Ignore this log and append another log", "Combine the previous logs"])
                if a == 0:
                    cont = True
                if a == 1:
                    exit()
                if a == 3:
                    sorted(logs, key=timesort)
                    for l in logs:
                        outlog += l
                    appending = False
            else:
                cont = True
            if cont:
                if options["m"] == "t":
                    maps.append(getmap(tmplog))
                if options["o"] == "t":
                    ids.append("https://logs.tf/" + u.path.split("/")[1])
                logs.append(clog)
                wholesize += len(clog.encode('utf-8'))
                a = optmenu("Do you want to", ["Append another log", "Combine the logs"])
                if a == 1:
                    sorted(logs, key=timesort)
                    for l in logs:
                        outlog += l
                    appending = False

        else:
            print("Invalid URL supplied - try again")
    print("Size of all logs: "+sizeof_fmt(wholesize))
    key = options["k"]
    print("Please enter a title for your log (max 40 characters)")
    title = input()

    if options["o"] == "t":
        outlog += outlog.split("\n")[-2][:24] + ' "Jack\'s Log Combiner<0><Console><Console>" say "The following logs were combined: ' + " & ".join(ids) + '"\n'

    mape = "Error"
    if options["m"] == "t":
        try:
            maps = list(OrderedDict.fromkeys(maps))
            if len(" + ".join(maps)) < 25:
                mape = " + ".join(maps)
            elif len(",".join(maps)) < 25:
                mape = ",".join(maps)
            else:
                nmaps = list()
                for m in maps:
                    p = m.split("_")
                    if len(p) == 2:
                        nmaps.append(p[1])
                    else:
                        nmaps.append("_".join(p[1:-1]))
                if len(" + ".join(nmaps)) < 25:
                    mape = " + ".join(nmaps)
                elif len(",".join(nmaps)) < 25:
                    mape = ",".join(nmaps)
                else:
                    raise Exception("We can't make the mapname small enough")

        except Exception:
            print("An error happened parsing the maps, please enter the map now yourself.")
            print("Please enter the maps (max 24 chars)")
            mape = input()
    else:
        print("Please enter the maps (max 24 chars)")
        mape = input()

    payload = {
        "title": title[0:40],
        "map": mape[0:24],
        "key": str(key),
        "uploader": "Jack's Log Combiner " + v + (" [Experimental]" if experimental else "")
    }

    files = {
        "logfile": StringIO(outlog)
    }
    r = requests.post("http://logs.tf/upload", data=payload, files=files)
    x = json.loads(r.text)
    if x["success"]:
        webbrowser.open_new_tab("https://www.logs.tf"+x["url"])
    else:
        print(r.text)

with open("version") as f:
    v = "v" + f.read()

options = {}
op = ["u", "m", "o", "k"]
if os.path.isfile("settings"):
    loadsettings()

else:
    o = []
    print("Seems like this is the first time using this script for you.")
    print("That's why you can choose some basic actions now.")
    if optmenu("Do you want that this script checks for updates?", ["Yes", "No"]) == 0:
        o.append("t")
    else:
        o.append("f")
    if optmenu("Do you want that this script tries to automatically generate the map names?", ["Yes", "No"]) == 0:
        o.append("t")
    else:
        o.append("f")
    if optmenu("Do you want that a chat message with the source logs is created?", ["Yes", "No"]) == 0:
        o.append("t")
    else:
        o.append("f")
    print("Please enter your Logs.tf API - Key")
    o.append(input())
    print("If you entered any wrong settings or want to change them, just delete the settings file.")
    outopt = "\n".join(o)
    with open("settings", "w") as s:
        s.write(outopt)
    loadsettings()

if options["u"] == "t":
    try:
        if LooseVersion(urllib2.urlopen("https://raw.githubusercontent.com/NetroScript/Jacks-TF2LogCombiner/master/version")) > LooseVersion(v[1:]):
            print("There is a new version available. Please download it at https://github.com/NetroScript/Jacks-TF2LogCombiner")
            if optmenu("Do you want to download the file now?", ["Yes", "No"]) == 0:
                webbrowser.open_new_tab("https://github.com/NetroScript/Jacks-TF2LogCombiner/archive/master.zip")
    except Exception:
        print("We were unable to check for updates")

interface()
