# jsonl-fstats - line delimited json fields statistics

jsonl-fstats is a Python3 program  that extracts some statistics regarding field coverage in a line delimited JSON document.

It reads from stdin and prints to stdout.

## Usage

```
jsonl-fstats 
        -help      print this help
        -marc      ignore Marc identifier field if you are analysing an index of marc records
        -headless  don't print headline
        -delimiter set which delimiter to use
```

## Requirements

numpy

e.g.
```
sudo apt-get install python3-numpy
```
