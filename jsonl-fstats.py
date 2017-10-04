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
def traverse(dict_or_list, path):
    if isinstance(dict_or_list, dict):
        iterator = dict_or_list.items()
    elif isinstance(dict_or_list,list):
        iterator = enumerate(dict_or_list)
    for k, v in iterator:
        yield path + str([k]), v
        if isinstance(v, (dict, list)):
            for k, v in traverse(v, path + str([k])):
                yield k, v
                    
                    
def str_max_map_len(array):
    try:
        return str(max(map(len,array)))
    except TypeError:
        return ""

def str_min_map_len(array):
    try:
        return str(min(map(len,array)))
    except TypeError:
        return ""

def removebraces(string):
    if string[-1]==']':
        string=string[:-1]
    if string[0]=='[':
        string=string[1:]
    return string

def isint(num):
    try: 
        int(num)
        return True
    except ValueError:
        return False

def getpercent(val,total):
    percent=(value)/float(hitcount)*100
    if percent>100:
        return 100
    else:
        return percent

def getnotexisting(value, hitcount):
    notexisting=hitcount-value
    if notexisting<0:
        return 0
    else:
        return notexisting

def marcString(string):
    stringarr=string.split("###")
    if(len(stringarr)==1) or '_' in stringarr[-1]:
        return ""
    string=stringarr[0]+" "+stringarr[-1]
    return string
        
    


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='return field statistics of an line-delimited JSON Document or Input-Stream')
    parser.add_argument('-marc',action="store_true",help='Ignore Marc Indicator')
    parser.add_argument('-help',action="store_true",help='print more help')
    parser.add_argument('-headless',action="store_true",help='don\'t print head')
    parser.add_argument('-delimiter',type=str,help='delimiter to use')
    args=parser.parse_args()
    hitcount=0
    if args.help:
        print("jsonl-fstats\n"\
"        -help      print this help\n"\
"        -marc      ignore Marc identifier field if you are analysing an index of marc records\n"\
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
        for key,val in traverse(jline,""):
            path=""
            fields=key.replace("'","").split("][")
            lastfield=removebraces(fields[-1])
            for field in fields:
                field=removebraces(field)
                if path:
                    if args.marc==False:
                        if isint(field):
                            continue
                        path=path+" > " +field
                    elif args.marc==True:
                        path=path+"###"+field
                else:
                    path=field
            if args.marc==True:
                path=marcString(path)
                if not path:
                    continue
            if path not in valstats:
                valstats[path]=dict()
            if path in valstats:
                if str(val) in valstats[path]:
                    valstats[path][str(val)]+=1
                else:
                    valstats[path][str(val)]={}
                    valstats[path][str(val)]=1
            if path not in stats:
                stats[path]=0
            if path in stats:
                stats[path]+=1
    if printhead:
        print("Total Records: "+str(hitcount))
        print("{:9s}{:1s}{:3s}{:1s}{:14s}{:1s}{:7s}{:1s}{:10s}{:1s}{:16s}{:1s}{:10s}{:1s}{:10s}{:1s}{:9s}{:1s}{:15s}{:1s}{:15s}{:1s}{:7s}{:1s}{:7s}{:1s}{:40s}".format("existing",delim,"%",delim,"notexisting",delim,"unique",delim,"avg",delim,"var",delim,"std",delim,"max",delim,"min",delim,"max-value",delim,"min-value",delim,"max-len",delim,"min-len",delim,"field name"))
    sortedstats=collections.OrderedDict(sorted(stats.items()))
    for key, value in sortedstats.items():
        if key in valstats: 
            unique=len(valstats[key])
            data=[]
            for obj in valstats[key]:
                data.append(valstats[key][obj])
        npdata = np.asarray(data)
        print("{:>9d}{:1s}{:>3.0f}{:1s}{:>14d}{:1s}{:>7d}{:1s}{:>10.2f}{:1s}{:>16.2f}{:1s}{:>10.2f}{:1s}{:>10d}{:1s}{:>9d}{:1s}{:>15s}{:1s}{:>15s}{:1s}{:>7s}{:1s}{:>7s}{:1s}{:<40s}".format(
                                                                    value,delim,
                                                                    getpercent(value,hitcount),delim,
                                                                    getnotexisting(value,hitcount),delim,
                                                                    unique,delim,
                                                                    np.mean(npdata),delim,
                                                                    np.var(npdata),delim,
                                                                    np.std(npdata),delim,
                                                                    max(data),delim,
                                                                    min(data),delim,
                                                                    str(max(valstats[key],key=lambda x: valstats[key][x]))[0:15],delim,
                                                                    str(min(valstats[key],key=lambda x: valstats[key][x]))[0:15],delim,
                                                                    str_max_map_len(valstats[key]),delim,
                                                                    str_max_map_len(valstats[key]),delim,
                                                                    key))
