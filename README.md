goalnotifier
============

A dirty hack to notify of any goals in ongoing Barcelona FC matches
Works in all UNIX based operating systems with the libnotify package.   
Works out-of-the-box in all Linux flavors

Usage
=====

When the game starts, run the score tracker as  

```
python scoretracker.py &
```
It will spring up notifications whenever a new goal is scored. It will also auto-exit when the game finishes.  
Just take care to not exit the terminal anywhere in between
