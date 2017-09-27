#!/usr/bin/python3 
# -*- coding: utf-8 -*-
from datetime import datetime
import collections
import json
from pprint import pprint
import numpy as np
import argparse
import sys

stats = dict()
valstats=dict()

printhead=True

def traverse(obj,path):
    global stats
    if isinstance(obj, dict):
        for key, value in obj.items():
            path=path+"_"+key
            if args.dc:
                path=key
            traverse(value,path)
    elif isinstance(obj, list):        
        if args.marc:
            for value in obj:
                traverse(value,path)
        if args.finc or args.dc:
            traverse(obj[0],path)
    else:
        if args.marc==True:
            if len(path)>3:
                if path[0]!='_':
                    marcpath=path[:3]+" "+path[-1:]
                    path = marcpath
        if path not in valstats:
            valstats[path]=dict()
        if path in valstats:
            if obj in valstats[path]:
                valstats[path][obj]+=1
            else:
                valstats[path][obj]={}
                valstats[path][obj]=1
        if path not in stats:
            stats[path]=1
        else:
            stats[path]+=1
        
if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='return field statistics of an line-delimited JSON Document or Input-Stream')
    parser.add_argument('-finc',action="store_true",help='Avoid >100% on analyzing finc data')
    parser.add_argument('-marc',action="store_true",help='Ignore Marc Indicator')
    parser.add_argument('-dc',action="store_true",help='Analyze dublin core data')
    parser.add_argument('-help',action="store_true",help='print more help')
    parser.add_argument('-headless',action="store_true",help='don\'t print head')
    parser.add_argument('-delimiter',type=str,help='delimiter to use')
    args=parser.parse_args()
    hitcount=1
    if args.help:
        print("jsonl-fstats\n"\
"        -help      print this help\n"\
"        -marc      ignore Marc identifier field if you are analysing an index of marc records\n"\
"        -finc      Avoid >100% on analyzing finc/dc data when multiple fields are assigned to one key\n"\
"        -dc        Analyze dublin core data\n"\
"        -headless  don't print headline\n"\
"        -delimiter set which delimiter to use\n")
        exit()
    if args.headless:
        printhead=False
    if args.delimiter is None:
        delim='|'
    else:
        delim=str(args.delimiter)
    for line in sys.stdin:
        try:
            jline=json.loads(line)
            hitcount+=1
        except ValueError:
            print("unclean jsonline: ")
            print(line)
            continue
        for field in jline:
            traverse(jline[field],field)
    if printhead:
        print("{:40s}{:1s}{:9s}{:1s}{:3s}{:1s}{:14s}{:1s}{:7s}{:1s}{:10s}{:1s}{:16s}{:1s}{:10s}{:1s}{:10s}{:1s}{:9s}{:1s}{:15s}{:1s}{:15s}{:1s}{:7s}{:1s}{:7s}".format("field name",delim,"existing",delim,"%",delim,"notexisting",delim,"unique",delim,"avg",delim,"var",delim,"std",delim,"max",delim,"min",delim,"max-value",delim,"min-value",delim,"max-len",delim,"min-len"))
        #print("----------------------------------------"+delim+"---------"+delim+"---"+delim+"--------------"+delim+"-------"+delim+"----------"+delim+"----------------"+delim+"----------"+delim+"----------"+delim+"---------"+delim+"---------------"+delim+"---------------"+delim+"-------"+delim+"-------")
    sortedstats=collections.OrderedDict(sorted(stats.items()))
    for key, value in sortedstats.items():
        if key in valstats: 
            unique=len(valstats[key])
            data=[]
            for obj in valstats[key]:
                data.append(valstats[key][obj])
        npdata = np.asarray(data)
        print("{:<40s}{:1s}{:>9d}{:1s}{:>3.0f}{:1s}{:>14d}{:1s}{:>7d}{:1s}{:>10.2f}{:1s}{:>16.2f}{:1s}{:>10.2f}{:1s}{:>10d}{:1s}{:>9d}{:1s}{:>15s}{:1s}{:>15s}{:1s}{:>7s}{:1s}{:>7s}".format(
                                                                    key,delim,
                                                                    value,delim,
                                                                    value/float(hitcount)*100,delim,
                                                                    hitcount-value,delim,
                                                                    unique,delim,
                                                                    np.mean(npdata),delim,
                                                                    np.var(npdata),delim,
                                                                    np.std(npdata),delim,
                                                                    max(data),delim,
                                                                    min(data),delim,
                                                                    str(max(valstats[key],key=lambda x: valstats[key][x]))[0:15],delim,
                                                                    str(min(valstats[key],key=lambda x: valstats[key][x]))[0:15],delim,
                                                                    str(max(map(len,valstats[key]))),delim,
                                                                    str(min(map(len,valstats[key])))))
