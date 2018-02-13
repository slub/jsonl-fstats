# jsonl-fstats - line delimited json fields statistics

jsonl-fstats is a Python3 program  that extracts some statistics regarding field coverage in a line delimited JSON document.

It reads from stdin and prints to stdout.

## Usage

```
jsonl-fstats.py 
        -help      print this help
        -marc      ignore Marc identifier field if you are analysing an index of marc records
        -headless  don't print headline
        -delimiter set which delimiter to use
```

* example with input and output file:
    ```
    jsonl-fstats.py < [INPUT LINE-DELIMITED JSON DOCUMENT] > [OUTPUT STATISTICS DOCUMENT]
    ```

## Requirements

[numpy](http://www.numpy.org/)

e.g. ```
apt-get install python3-numpy
```

## Run

* install numpy
* clone this git repo or just download the jsonl-fstats.py file
* run ./jsonl-fstats.py
* for a hackish way to use jsonl-fstats system-wide, copy to /usr/local/bin



### Install system-wide via pip

* via pip:
    ```
    sudo -H pip3 install --upgrade [ABSOLUTE PATH TO YOUR LOCAL GIT REPOSITORY OF JSONL-FSTATS]
    ```
    (which provides you ```jsonl-fstats``` as a system-wide commandline command)

