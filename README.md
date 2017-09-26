# jsonl-fstats - line delimited json fields statistics

jsonl-fstats is a Python program  that extracts some statistics regarding field coverage in a line delimited JSON document.

It reads from stdin and prints to stdout.

## Usage

```
jsonl-fstats 
        -help      print this help
        -marc      ignore Marc identifier field if you are analysing an index of marc records
        -finc      Avoid >100% on analyzing finc/dc data when multiple fields are assigned to one key
        -dc        Analyze dublin core data
        -headless  don't print headline
        -delimiter set which delimiter to use
```

