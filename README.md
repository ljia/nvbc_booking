# This script is to automatically book court at NVBC

site: https://nvbc.ezfacility.com/

## Installation

### Pre-requisites

1. Python 3 (script is tested with Python 3.9.6)
2. Chrome browser

### OS Supported

* Windows (script is tested with Windows 10 x64)
* Mac
* Linux

### Steps

1. Download and install [Python 3.9.6](https://www.python.org/downloads/)
2. Download and install Google Chrome
3. Install [pip](https://pip.pypa.io/en/stable/installation/)
4. Install required packages
```bash
pip install -r requirements.txt
```
5. Please download [ChromeDriver](https://chromedriver.chromium.org/downloads) for your OS 
and put it in the same directory where python executable resides.
**Note**: Please make sure to download the right version for your browser.

## Run Script

**Note**: The script does **NOT** support multi-thread. Please use appropriate tool to schedule and/or run multiple instances.
For example, the following script tries to open two browsers in Windows PowerShell:

```powershell
1,2 | ForEach-Object -Parallel { python.exe .\main.py -t 6PM --slot $_}
```

**Note**: The script does **NOT** give a confirmation if a court is successfully booked.
If you see 'clicked' in the console, that means the script successfully clicked the 'book' button.
It does NOT mean that a 'book' is guaranteed if multiple users are trying to book the same court at the same time.

### Steps

1. Before running, please update property.yml with your username/password.
2. To get help, run:
```bash
python main.py --help
```
3. To dry-run, run:
```bash
python.exe .\main.py -t 10AM --slot 1 --dry-run
```
The above example will try to book the 1st available courts at 10-11am (dry-run only)
3. To book court, run:
```bash
python.exe .\main.py -t 6PM --slot 3
```
The above example will try to book the 3rd available courts at 6-7pm