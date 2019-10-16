# TF2 Log Combiner
_____________________________________________
Like the name implies - this is a script to Combine Logs on https://www.logs.tf 

It is a command line application and it will (unlike other Log Combiners) try to minimize the log a bit.
Meaning you can fit more maps into a log. (Or at least that's the aim)

### Notes:  

If there are any errors shown feel free to send them to me, so I can fix them.
I made this on windows, but should also work on Linux.

If you don't like python you can alternatively find a userscript version directly for logs.tf [here](https://github.com/NetroScript/Jacks-LogsTF-On-Page-Combiner).


## Installation
_____________________________________________

* Download this as zip and extract it to the folder where you want it to be
* Get Python (3.X)
* Execute the file with `python main.py` (in the console with the folder where main.py resides as working directory - to simplify this just create a `run.bat` in the directory with the same content)
* Check if you get a module error (like: `ImportError: No module named '<module name>'`) if so then open a console (On Windows Win + R and type cmd and press enter) and type `python -m pip install <module name>`
* Enjoy

## Changelog
_____________________________________________


### 0.2.0

Added:
* Settings!
	* You can now enter your API Key at the first start and don't need to enter it again
	* The script can now try to automatically get the map names from the supplied logs
	* The script can now check for updates
	* The script can now add the links to the logs used to create the combined log in the chat

Fixed:
* Possible error with the read options when reading the downloaded logs - this happened because of different python versions
* Added some newlines for PEP 8


### 0.1.4

Fixed:
* The structure of 6s logs seem to differ compared to HL logs, meaning I added an additional check to my important part extractor 


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
