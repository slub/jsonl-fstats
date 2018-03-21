#!/usr/bin/python3 
# -*- coding: utf-8 -*-
import argparse
import collections
import csv
import json
import sys

import numpy as np

EXISTING = 'existing'
OCCURRENCE = 'occurrence'
EXISTING_PERCENTAGE = 'existing_percentage'
NOTEXISTING_PERCENTAGE = 'notexisting_percentage'
NOTEXISTING = 'notexisting'
UNIQUE = 'unique'
AVG = 'avg'
VAR = 'var'
STD = 'std'
MAX = 'max'
MIN = 'min'
MAX_VALUE = 'max_value'
MIN_VALUE = 'min_value'
MAX_LEN = 'max_len'
MIN_LEN = 'min_len'
FIELD_NAME = 'field_name'


def get_header():
    return [EXISTING,
            OCCURRENCE,
            EXISTING_PERCENTAGE,
            NOTEXISTING_PERCENTAGE,
            NOTEXISTING,
            UNIQUE,
            AVG,
            VAR,
            STD,
            MAX,
            MIN,
            MAX_VALUE,
            MIN_VALUE,
            MAX_LEN,
            MIN_LEN,
            FIELD_NAME]


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def traverse(obj, path):
    if isinstance(obj, dict):
        for k, v in obj.items():
            for c, w in traverse(v, path + "#!?#!?#!?" + str(k)):
                yield c, w
    elif isinstance(obj, list):
        for elem in obj:
            for c, w in traverse(elem, path + "#!?#!?#!?"):
                yield c, w
    if len(path) > 0 and not isinstance(obj, list):
        yield path, obj


def getname(string):
    array = string.rsplit("#!?#!?#!?")
    rstr = array[0]
    for elem in array[1:-1]:
        rstr = rstr + elem + " > "
    return rstr + array[-1]


def shortname(string):
    if string[-2:] == "> ":
        string = string[:-2]
    return string.replace(">  >", ">").strip()


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


def generate_field_statistics(statsmap, valstats, percentage_stats, hitcount, len_val):
    field_statistics = []
    for key, value in statsmap:
        unique = None
        if key in valstats:
            unique = len(valstats[key])
            data = []
            for obj in valstats[key]:
                data.append(valstats[key][obj])
        if len(data) > 0:
            npdata = np.asarray(data)
        else:
            npdata = np.asarray([0])

        field_statistic = {
            EXISTING: "{0:.0f}".format(percentage_stats[key]),
            OCCURRENCE: value,
            EXISTING_PERCENTAGE: "{0:.2f}".format(getpercent(percentage_stats[key], hitcount)),
            NOTEXISTING_PERCENTAGE: "{0:.2f}".format(
                getpercent(getnotexisting(percentage_stats[key], hitcount), hitcount)),
            NOTEXISTING: getnotexisting(value, hitcount),
            UNIQUE: unique,
            AVG: "{0:.2f}".format(np.mean(npdata)),
            VAR: "{0:.2f}".format(np.var(npdata)),
            STD: "{0:.2f}".format(np.std(npdata)),
            MAX: max(data, default=0),
            MIN: min(data, default=0),
            MAX_VALUE: str(max(valstats[key], key=lambda x: valstats[key][x], default=0)).strip()[0:int(len_val) - 2],
            MIN_VALUE: str(min(valstats[key], key=lambda x: valstats[key][x], default=0)).strip()[0:int(len_val) - 2],
            MAX_LEN: str_max_map_len(valstats[key]),
            MIN_LEN: str_max_map_len(valstats[key]),
            FIELD_NAME: key}

        field_statistics.append(field_statistic)

    return field_statistics


def simple_text_print(field_statistics, hitcount, headless, delimiter, len_val):
    if not headless:
        print("Total Records: " + str(hitcount))
        format_string = str(
            "{:8s}{:1s}{:9s}{:1s}{:6s}{:1s}{:6s}{:1s}{:14s}{:1s}{:7s}{:1s}{:10s}{:1s}{:16s}{:1s}{:10s}{:1s}{:10s}{:1s}{:9s}{:1s}" + "{:" + len_val + "s}" + "{:1s}" + "{:" + len_val + "s}" + "{:1s}{:7s}{:1s}{:7s}{:1s}{:40s}")
        print(format_string.format(
            "existing", delimiter,
            "occurrence", delimiter,
            "%", delimiter,
            "!%", delimiter,
            "notexisting", delimiter,
            "unique", delimiter,
            "avg", delimiter,
            "var", delimiter,
            "std", delimiter,
            "max", delimiter,
            "min", delimiter,
            "max-value", delimiter,
            "min-value", delimiter,
            "max-len", delimiter,
            "min-len", delimiter,
            "field name"))
    for field_statistic in field_statistics:
        format_string = str(
            "{:>8.0f}{:1s}{:>9d}{:1s}{:>6.2f}{:1s}{:>6.2f}{:1s}{:>14d}{:1s}{:>7d}{:1s}{:>10.2f}{:1s}{:>16.2f}{:1s}{:>10.2f}{:1s}{:>10d}{:1s}{:>9d}{:1s}" + "{:>" + len_val + "s}" + "{:1s}{:>" + len_val + "s}{:1s}{:>7s}{:1s}{:>7s}{:1s}{:<40s}")
        print(format_string.format(
            float(field_statistic[EXISTING]), delimiter,
            int(field_statistic[OCCURRENCE]), delimiter,
            float(field_statistic[EXISTING_PERCENTAGE]), delimiter,
            float(field_statistic[NOTEXISTING_PERCENTAGE]), delimiter,
            int(field_statistic[NOTEXISTING]), delimiter,
            int(field_statistic[UNIQUE]), delimiter,
            float(field_statistic[AVG]), delimiter,
            float(field_statistic[VAR]), delimiter,
            float(field_statistic[STD]), delimiter,
            int(field_statistic[MAX]), delimiter,
            int(field_statistic[MIN]), delimiter,
            '"' + field_statistic[MAX_VALUE] + '"', delimiter,
            '"' + field_statistic[MIN_VALUE] + '"', delimiter,
            field_statistic[MAX_LEN], delimiter,
            field_statistic[MIN_LEN], delimiter,
            '"' + field_statistic[FIELD_NAME] + '"'))


def csv_print(field_statistics):
    header = get_header()
    with sys.stdout as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, dialect='unix')

        writer.writeheader()
        for field_statistic in field_statistics:
            writer.writerow(field_statistic)


def run():
    parser = argparse.ArgumentParser(
        description='return field statistics of an line-delimited JSON Document or Input-Stream')
    parser.add_argument('-marc', action="store_true", help='Ignore Marc Indicator')
    parser.add_argument('-help', action="store_true", help='print more help')
    parser.add_argument('-headless', action="store_true", help='don\'t print header')
    parser.add_argument('-len_val', type=str, default="17",
                        help='specify the length for the values of "max-value" and "min-value"')
    parser.add_argument('-no_whitespace', default="|", type=str, help='don\'t count values only including whitespaces')
    parser.add_argument('-delimiter', default="|", type=str, help='delimiter to use')
    parser.add_argument('-csv-output', action="store_true",
                        help='prints the output as pure CSV data (all values are quoted)', dest='csv_output')
    args = parser.parse_args()
    if args.help:
        parser.print_usage(sys.stderr)
        exit(-1)
    hitcount = 0
    stats = {}
    percentage_stats = {}
    valstats = {}
    for line in sys.stdin:
        recordstats = []  # array to save the field paths per record, so we don't count paths twice (e.g. array-elements)
        try:
            jline = json.loads(line)
            hitcount += 1
        except ValueError:
            eprint("unclean jsonline: ")
            eprint(line)
            continue
        for key, val in traverse(jline, ""):
            if isinstance(val, str) and args.no_whitespace and (not val or val.isspace()):
                continue  # ignore vals which are lists or empty strings
            path = getname(key)
            if args.marc:
                array = key.rsplit("#!?#!?#!?")
                if len(array) >= 4:
                    array[3] = " > "
                    path = "".join(array)
            path = shortname(path)
            if path not in valstats:
                valstats[path] = {}
            if str(val) in valstats[path]:
                valstats[path][str(val)] += 1
            else:
                valstats[path][str(val)] = {}
                valstats[path][str(val)] = 1
            if path not in recordstats:  # append path to recordstats array by first iteration. after that, we ignore that path.
                recordstats.append(path)
                if path in percentage_stats:
                    percentage_stats[path] += 1
                else:
                    percentage_stats[path] = 1
            if path in stats:
                stats[path] += 1
            else:
                stats[path] = 1
            # eprint(path)
    sortedstats = collections.OrderedDict(sorted(stats.items()))
    field_statistics = generate_field_statistics(sortedstats.items(), valstats, percentage_stats, hitcount,
                                                 args.len_val)
    if not args.csv_output:
        simple_text_print(field_statistics, hitcount, args.headless, args.delimiter, args.len_val)
    else:
        csv_print(field_statistics)


if __name__ == "__main__":
    run()
