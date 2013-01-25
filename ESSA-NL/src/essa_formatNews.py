'''
Download, format and store news items

@author:  Sascha Holzhauer, CESR, Kassel, Germany
@date:    2011-04-21

History:  2011-04-11  (TOC, sorting, google download)
'''

import csv
import codecs
from cStringIO import StringIO
from operator import itemgetter
from essa_utils import *

def format(outputFile, issue, workingDir, user, password, debug, chapNum):
        
    # download as CVS to working dir
    downloadGoogleSpradsheet("News", issue, workingDir, user, password)
    
    inputFile = workingDir + issue + "/ESSA_NL_News.csv"
    
    reader = csv.DictReader(open(inputFile, 'rb'), delimiter=',', quotechar='"')
    
    outfile = open(outputFile, 'a')
    
    
    outfile.write('\n\n<h1><a name="news">' + str(chapNum) + '. News</a></h1>')
    outfile.write('<p>Note: News are ordered according to their title.</p>\n')
    
    
    file_str = StringIO()
   
    headerList = []
    
    # Sort items
    reader = sorted(filter(reader, issue), key=itemgetter('Title'))
    
    if len(reader) > 0:
        file_str.write("<table width=600>")
        
    for row in reader:
        if (debug == 1):
            print row
        file_str.write('<tr><td><a href="#toc_new">TOC</a></td><td class="con-title"><a name="new_' + str(len(headerList) + 1) + '">' + convert(row["Title"]) + "</a></td></tr>")
        headerList.append(convert(row["Title"]))
        processTaggs(file_str, convert(row["Taggs"]))   
        file_str.write('<tr class="odd"><td>' + "Content" + "</td><td>" + convert(row["Content"])  + "</td></tr>")
        file_str.write('<tr><td>' + "URL" + "</td><td>" + convert(row["URL"]) + "</td></tr>")
        file_str.write("<tr><td colspan=2><hr></td></tr>")
        
    if len(reader) > 0:
        file_str.write("</table>")
    
    subtoc(headerList, outfile, "new")
    
    outfile.write(file_str.getvalue())
    outfile.close()
    print("News: Done.")
