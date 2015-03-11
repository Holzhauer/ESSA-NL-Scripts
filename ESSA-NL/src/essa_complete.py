'''
Compiles different newsletter parts.

@author:  Sascha Holzhauer, CESR, Kassel, Germany
@date:    2011-04-21

History:
2011-04-25    - add dialog to enter issue number
2012-04-30    - cleaning

'''

import essa_formatJobs
import essa_formatNews
import essa_formatPublications
import essa_formatConferences
import essa_formatConferencesAttendance
#import essa_clipboardDateConvert

from Tkinter import Tk, Button, Label, W, Checkbutton, Entry, IntVar
import tkSimpleDialog
import tkMessageBox
import os
import sys

from essa_config import workingDir, logDir, user, sourceDir

loggingDir = logDir

if (not os.path.exists(loggingDir)):
    try:
        os.makedirs(loggingDir)
    except IOError:
        loggingDir = '~/Desktop'
        
sys.stdout = open(os.path.join(os.path.expanduser(loggingDir)) + "\\essa-nl.log", "w")
sys.stderr = open(os.path.join(os.path.expanduser(loggingDir)) + "\\essa-nl.log", "w")

password=""
issue = ""

debug = 0

class IssueDialog(tkSimpleDialog.Dialog):
    

    def body(self, top):

        self.title("Issue Number")
        Label(top, text="Enter issue number: ").grid(row=0, sticky=W)
        
        Label(top, text="Chapter number to start with: ").grid(row=1, sticky=W)
        
        Label(top, text="Enter password for " + user + ": ").grid(row=2, sticky=W)
        
        
        self.e1 = Entry(top)
        self.e1.insert(0, "000")
        self.e1.grid(row=0, column=1)
        
        self.e3 = Entry(top)
        self.e3.insert(0, "2")
        self.e3.grid(row=1, column=1)
        
        self.e2 = Entry(top, show="*")
        self.e2.grid(row=2, column=1)
        
        self.var = IntVar()
        self.b = Checkbutton(top, text="Debug?", variable= self.var, onvalue = 1, offvalue = 0)
        self.b.grid(row=3, columnspan=2, sticky=W)
        
        #def callConvert():
            #essa_clipboardDateConvert.convert()

        
        #self.convertButton = Button(top, text="Convert clipboard date", command=callConvert)
        #self.convertButton.grid(row=4, columnspan=2, sticky=W)



    def apply(self):
        global issue
        issue = self.e1.get()
        
        global chapNum
        chapNum = int(self.e3.get())
        
        global password
        password = self.e2.get()

        global debug
        debug = self.var.get()


# fetch issue number via dialog
root = Tk()
root.withdraw()
d = IssueDialog(root)

if (issue != ""):

    try:
        print "Processing issue", issue
        
        # create working dir if not existing:
        if not os.path.exists(workingDir):
            os.makedirs(workingDir)
        
        # open target file
        outputFile =  workingDir + issue + "/Newsletter.html"
        if (not os.path.exists(workingDir + issue)):
            os.makedirs(workingDir + issue)
        
        outFile = open(outputFile, "w")
        
        # copy preface etc.:
        inputFile = sourceDir + issue + "/content.html"
        if (os.path.exists(sourceDir + issue)):
            inputFile = sourceDir + issue + "/content.html"
        else:
            inputFile = sourceDir + "general" + "/content.html"
        infile = open(inputFile, 'r')
        input =  infile.readline()
        while input != "":
            outFile.write(input)
            input = input =  infile.readline()
        outFile.close()
        
        # generate parts:
        essa_formatNews.format(outputFile, issue, workingDir, user, password, debug, chapNum)
        
        essa_formatPublications.format(outputFile, issue, workingDir, user, password, debug, chapNum + 1)
        
        essa_formatJobs.format(outputFile, issue, workingDir, user, password, debug, chapNum + 2)
        
        essa_formatConferences.format(outputFile, issue, workingDir, user, password, debug, chapNum + 3)
        
        essa_formatConferencesAttendance.format(outputFile, issue, workingDir, user, password, debug, chapNum + 4)
        
        # copy footer:
        if (os.path.exists(sourceDir + issue)):
            inputFile = sourceDir + issue + "/footer.html"
        else:
            inputFile = sourceDir + "general" + "/footer.html"
        infile = open(inputFile, 'r')
        input =  infile.readline()
        outFile = open(outputFile, "a")
        while input != "":
            outFile.write(input)
            input = input =  infile.readline()
        
        outFile.close()
        print "Issue", issue, "done."
        tkMessageBox.showinfo("ESSA-NL", "Issue " + issue + " done. Files stored to " + workingDir + issue + ".")
    except:
        print "Unexpected error:", sys.exc_info()[0]
        tkMessageBox.showinfo("ESSA-NL", "Error occurred! See log file:" + str(sys.exc_info()[0]))
        raise
        