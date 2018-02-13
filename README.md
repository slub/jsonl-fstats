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

* example with input and output file:
    ```
    jsonl-fstats < [INPUT LINE-DELIMITED JSON DOCUMENT] > [OUTPUT STATISTICS DOCUMENT]
    ```

## Requirements

[argparse](https://docs.python.org/3/library/argparse.html#module-argparse)
[numpy](http://www.numpy.org/)

### Install Requirements

* via pip:
    ```
    sudo -H pip3 install --upgrade [ABSOLUTE PATH TO YOUR LOCAL GIT REPOSITORY OF JSONL-FSTATS]
    ```
    (which provides you ```jsonl-fstats``` as a system-wide commandline command)

* or ,e.g., for a Debian-based Linux system:
    ```
    sudo apt-get install python3-numpy
    ```
