'''
Converts dates in clipboard of the form mm/dd/yyyy into 'yyyy-mm-dd and copies
it back to clipboard.
 
@date:    2011-04-20
@author: Sascha Holzhauer
'''

import win32clipboard as w 

def getText(): 
    w.OpenClipboard() 
    d=w.GetClipboardData(w.CF_TEXT) 
    w.CloseClipboard() 
    return d 
 
def setText(aType,aString): 
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(aType,aString) 
    w.CloseClipboard()

def convert():
    text = getText()
    parts = text.split("/")
    setText(w.CF_TEXT, "'" + parts[2] + "-%02d-%02d" % (int(parts[0]), int(parts[1])))