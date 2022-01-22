# MalAPIReader
Parses API entries and prints information from the website [MalAPI.io](https://malapi.io/)

## Setup
Clone the repo:
```
$ git clone https://github.com/HuskyHacks/MalAPIReader.git && cd MalAPIReader
```
Install Poetry:
```
$ pip3 install poetry
```
Enter Poetry shell:
```
$ poetry shell
```
Install dependencies:
```
$ poetry install
```
Run the script:
```
$ python3 MalAPIReader.py -h
```
## Usage
``` 
usage: MalAPIReader.py [-h] [--pe PE] [--look LOOK] [--verbose] [--report]

Read information from MalAPI.io for WinAPI information.

optional arguments:
  -h, --help            show this help message and exit
  --pe PE, -p PE        Specify a PE to read. The WinAPI will be checked against MalAPI and information will be printed about the API if the information is present.
  --look LOOK, -l LOOK  Look up an API by name and print all information.
  --verbose, -v         Increase verbosity of output
  --report, -r          Write report to the reports directory
```
  
  The `--look` option takes one argument: the name of an API. It will then make a request for the basic details about the API from MalAPI.io and print it. In the example below, we pass "ShellExecuteA" as an argument and receive information back.

i.e.

![image](https://user-images.githubusercontent.com/57866415/148666662-eb041406-cac1-4be5-a9e6-8c2d60ad48d3.png)


  The `--pe` option takes one argument: the path and name to an PE file. It will then read the Import Address Table and check for any entries on MalAPI.io. If an entry is found, information about the API is then printed.

i.e.

![image](https://user-images.githubusercontent.com/57866415/148666776-c9ff5d00-3c78-4360-a82a-a72986507e7e.png)
![image](https://user-images.githubusercontent.com/57866415/148666780-a0d254c5-49e0-4846-94ab-e585fd17ce09.png)


The `-r` option writes the console out to a date-time stamped logfile in `reports/` for later retrieval.

## Known Bug
Keyboard Interrupts are not reliable. I am able to interrupt when running from IDLE but not when running from cmd.exe

The `--report` arg and the `--verbose` arg create strange log entries due to the use of colorama. All of the data is in there but the colors render as unprintable chars.

## Thanks
Thank you mr.d0x for the inspiring project.
