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

e.g. 
```
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
    

## Erklärung der Spaltenköpfe

### Total Records:
* gibt an, über wieviele Rekords (=Zeilen) die Datei verfügt

### existing
* gibt an, wieviele Felder diesen Pfades existieren.

### occurence
* gibt an, wieviele Werte diesen Pfades vorhanden sind. (Mehrfachbelegung)

### %
* existing in Prozent
* existing / Total Records * 100

### !%
* notexisting in Prozent
* notexisting / Total Records * 100)

### not existing
* gibt an, wieviele Rekords nicht über diesen Pfad verfügen

### unique
* gibt an, wieviele einzigartige Werte man in diesem Pfad findet

### avg
* gibt an, wie oft man im Schnitt einen Wert in diesem Pfad findet

### std
* Standardabweichung der Häufigkeit der Werte in diesem Pfad

### max
* Maximale Anzahl eines Wertes in diesem Pfad

### min
* Minimale Anzahl eines Wertes in diesem Pfad

### max-value
* Der Wert, welcher am häufigsten in diesem Pfad vorkommt
* Ausgabe ist auf 17 Stellen gekürzt, kann mit dem Schalter -var_len angepasst werden

### min-value
* Der Wert, welcher am wenigsten in diesem Pfad vorkommt
* Ausgabe ist auf 17 Stellen gekürzt, kann mit dem Schalter -var_len angepasst werden

### max-len
* Die Zeichenanzahl des längsten Wertes in diesem Pfad

### min-len
* Die Zeichenanzahl des kürzesten Wertes in diesem Pfad

### field name
* Der Pfad zu den analysierten Werten
