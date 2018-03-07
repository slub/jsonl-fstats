#!/usr/bin/python3 
# -*- coding: utf-8 -*-
import argparse
import collections
import json
import sys
import numpy as np

        
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def traverse(dict_or_list, path):
    iterator=None
    if isinstance(dict_or_list, dict):
        iterator = dict_or_list.items()
    elif isinstance(dict_or_list, list):
        iterator = enumerate(dict_or_list)
    else:
        yield path,dict_or_list
    if iterator:
        for k, v in iterator:
            if isinstance(dict_or_list,dict):
                yield path + str([k]), v
                for k, v in traverse(v, path + str([k])):
                    yield k, v
            elif isinstance(dict_or_list,list):
                yield path, v
                for k, v in traverse(v, path):
                    yield k, v
#        if isinstance(v, (dict, list)):
#            for k, v in traverse(v, path + str([k])):
#                yield k, v


def str_max_map_len(array):
    return str(max(map(len, array), default=0))

def str_min_map_len(array):
    return str(min(map(len, array), default=0))
    
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
    return (value) / float(hitcount) * 100


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
    parser.add_argument('-len_val', type=str,default="17", help='don\'t print head')
    parser.add_argument('-no_whitespace', default="|", type=str, help='don\'t count val with whitespacewhitespace')
    parser.add_argument('-delimiter', default="|", type=str, help='delimiter to use')
    args = parser.parse_args()
    if args.help:
        parser.print_usage(sys.stderr)
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
            path = ""
            fields = key.replace("'", "").split("][")
            lastfield = removebraces(fields[-1])
            for field in fields:
                field = removebraces(field)
                if path:
                    if args.marc:
                        path = path + "###" + field
                    else:
                        path = path + " > " + field
                else:
                    path = field
            if args.marc:
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
                "occurence", args.delimiter,
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
