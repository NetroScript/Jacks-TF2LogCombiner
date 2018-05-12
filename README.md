# TF2 Log Combiner
_____________________________________________
Like the name implies - this is a script to Combine Logs on https://www.logs.tf 

It is a command line application and it will (unlike other Log Combiners) try to minimize the log a bit.
Meaning you can fit more maps into a log. (Or at least that's the aim)

### Notes:  

If there are any errors shown feel free to send them to me, so I can fix them.
I made this on windows, but should also work on Linux.


If you get an error like this:
```python
Traceback (most recent call last):
  File "C:\Users\User\Documents\LogsTF Combiner\Jacks-TF2LogCombiner-master\main.py", line 163, in <module>
    interface()
  File "C:\Users\User\Documents\LogsTF Combiner\Jacks-TF2LogCombiner-master\main.py", line 115, in interface
    clog = get_important(getlog(tmplog), experimental)
  File "C:\Users\User\Documents\LogsTF Combiner\Jacks-TF2LogCombiner-master\main.py", line 63, in getlog
    with myzipfile.open(name, "rU") as readfile:
  File "E:\Programs\Python\lib\zipfile.py", line 1334, in open
    raise ValueError('open() requires mode "r" or "w"')
ValueError: open() requires mode "r" or "w"
```

Then replace `        with myzipfile.open(name, "rU") as readfile:` with `        with myzipfile.open(name, "r") as readfile:`


## Installation
_____________________________________________

* Download this as zip and extract it to the folder where you want it to be
* Get Python (3.X)
* Execute the file with `python main.py` (in the console with the folder where main.py resides as working directory - to simplify this just create a `run.bat` in the directory with the same content)
* Check if you get a module error (like: `ImportError: No module named '<module name>'`) if so then open a console (On Windows Win + R and type cmd and press enter) and type `python -m pip install <module name>`
* Enjoy

## Changelog
_____________________________________________


### 0.1.3

Fixed:
* It would not combine logs which were combined before by this program
* The API doesn't seem to enforce 5MB, meaning now the program allows you to upload logs > 5MB should you want to. 


### 0.1.2

Fixed:
* Improved Experimental mode (Now removes useless trigger events | FYI The experimental mode works the same as the normal one but might fuck up names)


### 0.1.1

Fixed:
* Ignore unexpected newlines


### 0.1

* Released


## Planned features
_____________________________________________

* Maybe a GUI and saving some Settings
