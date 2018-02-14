#!/usr/bin/python3 
# -*- coding: utf-8 -*-
import argparse
import collections
import json
import sys
import numpy as np

def traverse(dict_or_list, path):
    if isinstance(dict_or_list, dict):
        iterator = dict_or_list.items()
    elif isinstance(dict_or_list, list):
        iterator = enumerate(dict_or_list)
    for k, v in iterator:
        yield path + str([k]), v
        if isinstance(v, (dict, list)):
            for k, v in traverse(v, path + str([k])):
                yield k, v

def str_max_map_len(array):
    try:
        return str(max(map(len, array), default=0))
    except TypeError:
        return ""

def str_min_map_len(array):
    try:
        return str(min(map(len, array), default=0))
    except TypeError:
        return ""

def removebraces(string):
    if string[-1] == ']':
        string = string[:-1]
    if string[0] == '[':
        string = string[1:]
    return string

def isint(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def getpercent(value, hitcount):
    percent = (value) / float(hitcount) * 100
    if percent > 100:
        return 100
    else:
        return percent

def getnotexisting(value, hitcount):
    notexisting = hitcount - value
    if notexisting < 0:
        return 0
    else:
        return notexisting

def marcString(string):
    stringarr = string.split("###")
    if (len(stringarr) == 1) or '_' in stringarr[-1]:
        return ""
    string = stringarr[0] + " " + stringarr[-1]
    return string

def run():
    parser = argparse.ArgumentParser(
        description='return field statistics of an line-delimited JSON Document or Input-Stream')
    parser.add_argument('-marc', action="store_true", help='Ignore Marc Indicator')
    parser.add_argument('-help', action="store_true", help='print more help')
    parser.add_argument('-headless', action="store_true", help='don\'t print head')
    parser.add_argument('-delimiter',default="|",type=str, help='delimiter to use')
    args = parser.parse_args()
    if args.help:
        print("jsonl-fstats\n" \
              "        -help      print this help\n" \
              "        -marc      ignore Marc identifier field if you are analysing an index of marc records\n" \
              "        -headless  don't print headline\n" \
              "        -delimiter set which delimiter to use\n")
        exit()
    hitcount = 0
    stats = {}
    valstats = {}

    for line in sys.stdin:
        try:
            jline = json.loads(line)
            hitcount += 1
        except ValueError:
            print("unclean jsonline: ")
            print(line)
            continue
        for key, val in traverse(jline, ""):
            if isinstance(val, list):
                continue
            path = ""
            fields = key.replace("'", "").split("][")
            lastfield = removebraces(fields[-1])
            for field in fields:
                field = removebraces(field)
                if path:
                    if args.marc == False:
                        if isint(field):
                            continue
                        path = path + " > " + field
                    elif args.marc == True:
                        path = path + "###" + field
                else:
                    path = field
            if args.marc == True:
                path = marcString(path)
                if not path:
                    continue
                if path[-2] != ' ':
                    continue
                if path[-1] != '0' and isint(path[-1]) and int(path[0:3]) > 10:
                    continue
            if path in valstats:
                if str(val) in valstats[path]:
                    valstats[path][str(val)] += 1
                else:
                    valstats[path][str(val)] = {}
                    valstats[path][str(val)] = 1
            else:
                valstats[path] = {}
            if path in stats:
                stats[path] += 1
            else:
                stats[path] = 0
    if not args.headless:
        print("Total Records: " + str(hitcount))
        print(
            "{:9s}{:1s}{:3s}{:1s}{:14s}{:1s}{:7s}{:1s}{:10s}{:1s}{:16s}{:1s}{:10s}{:1s}{:10s}{:1s}{:9s}{:1s}{:17s}{:1s}{:17s}{:1s}{:7s}{:1s}{:7s}{:1s}{:42s}".format(
                "existing", args.delimiter, "%", args.delimiter, "notexisting", args.delimiter, "unique", args.delimiter, "avg", args.delimiter, "var", args.delimiter, "std",
                args.delimiter, "max", args.delimiter, "min", args.delimiter, "max-value", args.delimiter, "min-value", args.delimiter, "max-len", args.delimiter, "min-len",
                args.delimiter, "field name"))
    sortedstats = collections.OrderedDict(sorted(stats.items()))
    for key, value in sortedstats.items():
        if key in valstats:
            unique = len(valstats[key])
            data = []
            for obj in valstats[key]:
                data.append(valstats[key][obj])
        npdata = np.asarray(data)
        print(
            "{:>9d}{:1s}{:>3.0f}{:1s}{:>14d}{:1s}{:>7d}{:1s}{:>10.2f}{:1s}{:>16.2f}{:1s}{:>10.2f}{:1s}{:>10d}{:1s}{:>9d}{:1s}{:>17s}{:1s}{:>17s}{:1s}{:>7s}{:1s}{:>7s}{:1s}{:<42s}".format(
                value, args.delimiter,
                getpercent(value, hitcount), args.delimiter,
                getnotexisting(value, hitcount), args.delimiter,
                unique, args.delimiter,
                np.mean(npdata), args.delimiter,
                np.var(npdata), args.delimiter,
                np.std(npdata), args.delimiter,
                max(data, default=0), args.delimiter,
                min(data, default=0), args.delimiter,
                '"' + str(max(valstats[key], key=lambda x: valstats[key][x], default=0))[0:15] + '"', args.delimiter,
                '"' + str(min(valstats[key], key=lambda x: valstats[key][x], default=0))[0:15] + '"', args.delimiter,
                str_max_map_len(valstats[key]), args.delimiter,
                str_max_map_len(valstats[key]), args.delimiter,
                '"' + key + '"'))

if __name__ == "__main__":
    run()
