# Screen-Shot-Cleanup

## Table of contents
* [General info](#general-info)
* [Requirements](#requirements)
* [Setup](#setup)

## General info
MacOS saves screenshots by default on the Desktop. I'm always apprehensive about
deleting these so soon as so they accumulate. I wanted an automated way of
removing them after a time by which I'm sure I don't need them anymore.

This script will install a daemon that will remove any screenshots
from the desktop that haven't been accessed in 30 days or more.

This script can also be run on it's own to remove screen shot files, but
ensure the plist is not in the current path.

Target file example: "Screen Shot 2020-09-30 at 9.48.25 PM.png"
	
## Requirements

* Python3

	
## Setup
To run this project, clone it or download it to a suitable location and 
run it from a terminal:

```
$ python3 screen_shot_cleanup.py
```
You are good to go!
Logs of removed screenshots can be found in `~/Library/Logs/Screen Shot Cleanup.log`