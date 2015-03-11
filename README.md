ESSA-NL-Scripts
===============

A set scripts that help preparing the ESSA Newsletter for the editors Editors, originally written by Sascha Holzhauer (CESR, Kassel, Germany).

The European Social Simulation Association ([http://essa.eu.org/](http://essa.eu.org/)) Newsletter is sent out every two weeks, containing the most relevant information to their members.

Previous releases are available for the members at the ESSA Site after logging in:

[http://www.essa.eu.org/newsletter](http://www.essa.eu.org/newsletter)

To submitt content for the next issue, use the google forms that allow everyone to enter in information about conferences, publications, job offers, and news, which helps us saving a lot of effort and ensures that the right information is at the right place. Do not forget to leave a name and email address in the "Other" field when you submit content:

* [Calls for Papers or Proposals for Conferences, Meetings, Symposia, and Journals](https://spreadsheets.google.com/viewform?formkey=dEJRRkF1ZGJXWHVvSXlpQTg5QUoxQXc6MQ)
* [Calls for Attendance for Conferences, Workshops, Meetings and Symposia](https://spreadsheets.google.com/viewform?hl=en&hl=en&formkey=dFdmLW9panBaTDN2MWdXR0RFQVhVM0E6MQ#gid=0)
* [Job Offers](https://spreadsheets.google.com/viewform?hl=en&formkey=dGh2Sk9EcW16eUxPU3gtQUtkWkhrY1E6MQ#gid=0)
* [Publications](https://spreadsheets.google.com/viewform?formkey=dHY1Z1AyTFZWZFNSbmx5YThNNDltbXc6MQ)
* [News](https://spreadsheets.google.com/viewform?hl=en&formkey=dGFzdlcteHhOWGlqaXVKUEtOWkx0UVE6MQ#gid=0)


## Installation ##
Use the setup.exe in ./dist/Output to install the program on windows machines.
Change at least the username in essanl.config (see below)

## Configuration Issues ##
Configuration is done via ./config/essanl.config. Note that you need to change permission in case you installed ESSA-NL in your program folder.

### [basic] ###
username=\[user\]
> Specify your google username that grants you access to the ESSA-NL google forms \*

sourceDir=./ESSA-NL/
> Directory that contains subfolders with the HTML header and footer (\[issue-number\]
> to be used for a specific issue and "general" to be used if no special folder names <issue-number> exists)

destination=./
> Target directory for downloaded google forms and the resulting HTML file.

logDir=./Loggings
> Log files are placed here.

### [behaviour] ###
replace_unicode_encode_error=0
> Has currently no effect

----------------------
\* mandatory to specify. For all other entries defaults should work.

## Developing and Building the ESSA-Newsletter-Scripts ##

### Requirements to develop ###
* Python Interpreter (http://python.org/download/)
* gdata google python API (https://github.com/google/gdata-python-client)
* Py2Exe to build python independent executable (http://www.py2exe.org/)
* Inno Setup to compile the Setup.Exe (http://www.jrsoftware.org/isinfo.php)

### Building ###
cd ./ESSA-NL/src/bild
python setup.py py2exe 

Hints:
* Make sure the essa_* modules are on the PYTHONPATH
* In eclipse, you might want to use launcher/ESSA-NL setup.py.launch
* You might need to call it a second time in case InnoSetup raises an error during the first run)

## Changelog ##

### version 1.1 ###
* Bugfix in gdata due to changes in google API
* Dialog to confirm the program has ended
* Handling user directory indicated by "~"

## TODO ##
* allow changing of essanl.config location
* see scripts
