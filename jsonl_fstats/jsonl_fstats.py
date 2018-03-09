#!/usr/bin/python3 
# -*- coding: utf-8 -*-
import argparse
import collections
import json
import sys
import numpy as np

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def traverse(obj,path):
    if isinstance(obj,dict):
        for k,v in obj.items():
            for c,w in traverse(v,path+"#!?#!?#!?"+str(k)):
                yield c,w
    elif isinstance(obj,list):
        for elem in obj:
            for c,w in traverse(elem,str(path)):
                yield c,w
    else:
        yield path,obj

def getname(string):
    array=string.rsplit("#!?#!?#!?")
    rstr=array[0]
    for elem in array[1:-1]:
        rstr=rstr+elem+" > "
    return rstr+array[-1]

def str_max_map_len(array):
    return str(max(map(len, array), default=0))

def str_min_map_len(array):
    return str(min(map(len, array), default=0))

def getpercent(value, hitcount):
    return (value) / float(hitcount) * 100

def getnotexisting(value, hitcount):
    notexisting = hitcount - value
    if notexisting < 0:
        return 0
    else:
        return notexisting

def run():
    parser = argparse.ArgumentParser(
        description='return field statistics of an line-delimited JSON Document or Input-Stream')
    parser.add_argument('-marc', action="store_true", help='Ignore Marc Indicator')
    parser.add_argument('-help', action="store_true", help='print more help')
    parser.add_argument('-headless', action="store_true", help='don\'t print head')
    parser.add_argument('-len_val', type=str,default="17", help='don\'t print head')
    parser.add_argument('-no_whitespace', default="|", type=str, help='don\'t count val with whitespacewhitespace')
    parser.add_argument('-delimiter', default="|", type=str, help='delimiter to use')
    args = parser.parse_args()
    if args.help:
        parser.print_usage(sys.stderr)
        exit(-1)
    hitcount = 0
    stats = {}
    percentage_stats={}
    valstats = {}
    for line in sys.stdin:
        recordstats=[]      #array to save the field paths per record, so we don't count paths twice (e.g. array-elements)
        try:
            jline = json.loads(line)
            hitcount += 1
        except ValueError:
            eprint("unclean jsonline: ")
            eprint(line)
            continue
        for key, val in traverse(jline, ""):
            if isinstance(val, list) or (isinstance(val,str) and args.no_whitespace and (not val or val.isspace())):
                continue #ignore vals which are lists or empty strings
            path=getname(key)
            if args.marc:
                array=key.rsplit("#!?#!?#!?")
                if len(array)>=4:
                    del array[2]
                    path="".join(array)
            if path not in valstats:
                valstats[path]={}
            if str(val) in valstats[path]:
                valstats[path][str(val)] += 1
            else:
                valstats[path][str(val)] = {}
                valstats[path][str(val)] = 1
            if path not in recordstats: #append path to recordstats array by first iteration. after that, we ignore that path.
                recordstats.append(path)
                if path in percentage_stats:
                    percentage_stats[path] += 1
                else:
                    percentage_stats[path] = 1
            if path in stats:
                stats[path] += 1
            else:
                stats[path] = 1
    if not args.headless:
        print("Total Records: " + str(hitcount))
        format_string=str("{:8s}{:1s}{:9s}{:1s}{:6s}{:1s}{:6s}{:1s}{:14s}{:1s}{:7s}{:1s}{:10s}{:1s}{:16s}{:1s}{:10s}{:1s}{:10s}{:1s}{:9s}{:1s}"+"{:"+args.len_val+"s}"+"{:1s}"+"{:"+args.len_val+"s}"+"{:1s}{:7s}{:1s}{:7s}{:1s}{:40s}")
        print(format_string.format(
                "existing", args.delimiter,
                "occurrence", args.delimiter,
                "%", args.delimiter,
                "!%", args.delimiter,
                "notexisting", args.delimiter,
                "unique", args.delimiter, 
                "avg", args.delimiter, 
                "var", args.delimiter, 
                "std",args.delimiter, 
                "max", args.delimiter, 
                "min", args.delimiter, 
                "max-value",args.delimiter, 
                "min-value",args.delimiter, 
                "max-len", args.delimiter, 
                "min-len", args.delimiter, 
                "field name"))
    sortedstats = collections.OrderedDict(sorted(stats.items()))
    for key, value in sortedstats.items():
        if key in valstats:
            unique = len(valstats[key])
            data = []
            for obj in valstats[key]:
                data.append(valstats[key][obj])
        if len(data) > 0:
            npdata = np.asarray(data)
        else:
            npdata = np.asarray([0])
        format_string=str("{:>8.0f}{:1s}{:>9d}{:1s}{:>6.2f}{:1s}{:>6.2f}{:1s}{:>14d}{:1s}{:>7d}{:1s}{:>10.2f}{:1s}{:>16.2f}{:1s}{:>10.2f}{:1s}{:>10d}{:1s}{:>9d}{:1s}"+"{:>"+args.len_val+"s}"+"{:1s}{:>"+args.len_val+"s}{:1s}{:>7s}{:1s}{:>7s}{:1s}{:<40s}")
        print(format_string.format(
                percentage_stats[key], args.delimiter,
                value, args.delimiter,
                getpercent(percentage_stats[key], hitcount), args.delimiter,
                getpercent(getnotexisting(percentage_stats[key], hitcount),hitcount),args.delimiter,
                getnotexisting(value, hitcount), args.delimiter,
                unique, args.delimiter,
                np.mean(npdata), args.delimiter,
                np.var(npdata), args.delimiter,
                np.std(npdata), args.delimiter,
                max(data, default=0), args.delimiter,
                min(data, default=0), args.delimiter,
                '"' + str(max(valstats[key], key=lambda x: valstats[key][x], default=0)).strip()[0:int(args.len_val)-2] + '"', args.delimiter,
                '"' + str(min(valstats[key], key=lambda x: valstats[key][x], default=0)).strip()[0:int(args.len_val)-2] + '"', args.delimiter,
                str_max_map_len(valstats[key]), args.delimiter,
                str_max_map_len(valstats[key]), args.delimiter,
                '"' + key + '"'))

if __name__ == "__main__":
    run()
