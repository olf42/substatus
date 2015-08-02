# Substatus

This script can be used to monitor the open/closed state of 
hackerspaces around the world to create heatmaps, predict opening times, ...

It fetches all hackerspaces participating in the space api project, and is then called periodically with a cronjob, or whatever floats your boat when it comes to periodic task execution.

# Requirements

* sqlite3

# Known Bugs

* The list of participating hackerspaces is fetched upon database creation and cannot be updated. :(
