Developing and Building the ESSA-Newsletter-Scripts

@author Sascha Holzhauer, CESR (holzhauer@cesr.de)
@date	27/04/2012


:: Requirements to develop ::
Python Interpreter (http://python.org/download/)
Py2Exe to build python independent executable (http://www.py2exe.org/)
Inno Setup to compile the Setup.Exe (http://www.jrsoftware.org/isinfo.php)

:: Installation ::
Use the setup.exe in ./dist to install the program on windows maschines.

:: Configuration Issues ::
Configuration is done via ./config/essanl.config.
----------------------
[basic]
username=<user>
	> Specify your google username that grants you access to the ESSA-NL google forms *
sourceDir=./ESSA-NL/
	> Directory that contains subfolders with the HTML header and footer (<issue-number> 
	> to be used for a specific isuue and "general" to be used if no special folder names <issue-number> exists)
destination=./
	> Target directory for downloaded google forms and the resulting HTML file.
logDir=./Loggings
	> Log files are placed here.

[behaviour]
replace_unicode_encode_error=0
	> Has currently no effect
----------------------
* mandatory to specify. For all other entries defaults should work.

:: TODO ::
- see scripts