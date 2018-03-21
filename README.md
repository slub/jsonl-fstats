# jsonl-fstats - line delimited json fields statistics

jsonl-fstats is a Python3 program  that extracts some statistics regarding field coverage in a line delimited JSON document.

It reads from stdin and prints to stdout.

## Usage

```
jsonl-fstats.py 
        -h, --help                      show this help message and exit
        -marc                           Ignore Marc Indicator
        -help                           print more help
        -headless                       don't print header
        -len_val LEN_VAL                specify the length for the values of "max-value" and "min-value"
        -no_whitespace NO_WHITESPACE    don't count values only including whitespaces
        -delimiter DELIMITER            delimiter to use
        -csv-output                     prints the output as pure CSV data (all values are quoted)
```

* example with input and output file:
    ```
    jsonl-fstats.py < [INPUT LINE-DELIMITED JSON DOCUMENT] > [OUTPUT STATISTICS DOCUMENT]
    ```

## Requirements

[numpy](http://www.numpy.org/)

e.g. 
```
apt-get install python3-numpy
```

## Run

* install numpy
* clone this git repo or just download the [jsonl_fstats.py](jsonl_fstats/jsonl_fstats.py) file
* run ./jsonl_fstats.py
* for a hackish way to use jsonl-fstats system-wide, copy to /usr/local/bin



### Install system-wide via pip

* via pip:
    ```
    sudo -H pip3 install --upgrade [ABSOLUTE PATH TO YOUR LOCAL GIT REPOSITORY OF JSONL-FSTATS]
    ```
    (which provides you ```jsonl-fstats``` as a system-wide commandline command)
    

## Description

(of the column headers of a resulting statistic)

### ... in English

#### Total Records:
* total record count of the input

#### existing
* number of records that contain this field (path), i.e., field coverage

#### occurrence
* total count of the occurrence of this field (path) over all records, i.e., an indicator for field where multiple values are allowed

#### %
* ^ percentage of 'existing'
* (existing / Total Records * 100)

#### !%
* ^ percentage of 'notexisting'
* (not existing / Total Records * 100)

#### notexisting
* number of records that do not contain this field (path)

#### unique
* number of unique/distinct values of this field (path), i.e., cardinality

#### avg
* average occurrence of a value/values of this field (path) over all records

#### std
* standard variation of a value/values of this field (path) over all records

#### max
* maximum count of a (unique/distinct) value of this field (path) over all records

#### min
* minimum count of a (unique/distinct) value of this field (path) over all records

#### max-value
* the concrete value of 'max', i.e., the most frequently used value
* the output is trimmed per default to max 17 character; you can change this string length with the option -var_len

#### min-value
* the concrete value of 'min', i.e., the least frequently used value
* the output is trimmed per default to max 17 character; you can change this string length with the option -var_len

#### max-len
* the number of characters of the longest string of this field (path)

#### min-len
* the number of characters of the shortest string of this field (path)

#### field name
* the field (path) of this statistic line

### ... in German

Erklärung der Spaltenköpfe

#### Total Records:
* gibt an, über wieviele Rekords (=Zeilen) die Datei verfügt

#### existing
* gibt an, wieviele Felder diesen Pfades existieren.

#### occurrence
* gibt an, wieviele Werte diesen Pfades vorhanden sind. (Mehrfachbelegung)

#### %
* existing in Prozent
* existing / Total Records * 100

#### !%
* notexisting in Prozent
* notexisting / Total Records * 100)

#### notexisting
* gibt an, wieviele Rekords nicht über diesen Pfad verfügen

#### unique
* gibt an, wieviele einzigartige Werte man in diesem Pfad findet

#### avg
* gibt an, wie oft man im Schnitt einen Wert in diesem Pfad findet

#### std
* Standardabweichung der Häufigkeit der Werte in diesem Pfad

#### max
* Maximale Anzahl eines Wertes in diesem Pfad

#### min
* Minimale Anzahl eines Wertes in diesem Pfad

#### max-value
* Der Wert, welcher am häufigsten in diesem Pfad vorkommt
* Ausgabe ist auf 17 Stellen gekürzt, kann mit dem Schalter -var_len angepasst werden

#### min-value
* Der Wert, welcher am wenigsten in diesem Pfad vorkommt
* Ausgabe ist auf 17 Stellen gekürzt, kann mit dem Schalter -var_len angepasst werden

#### max-len
* Die Zeichenanzahl des längsten Wertes in diesem Pfad

#### min-len
* Die Zeichenanzahl des kürzesten Wertes in diesem Pfad

#### field name
* Der Pfad zu den analysierten Werten
