'''
Download, format and store publication items

@author:  Sascha Holzhauer, CESR, Kassel, Germany
@date:    2011-04-21

History:  2011-04-11  (TOC, sorting, google download)
'''

import csv

from essa_utils import *
from operator import itemgetter
from cStringIO import StringIO


def format(outputFile, issue, workingDir, user, password, debug, chapNum):

    # download as CVS to working dir
    downloadGoogleSpradsheet("Publications", issue, workingDir, user, password)
    
    inputFile = workingDir + issue + "/ESSA_NL_Publications.csv"
    
    reader = csv.DictReader(open(inputFile, 'rb'), delimiter=',', quotechar='"')
    
    outfile = open(outputFile, 'a')
    
    
    outfile.write('\n\n<h1><a name="pub">' + str(chapNum) + '. Publications</a></h1>')
    outfile.write('<p>Note: Publications are ordered according to their title.</p>\n')
    
    file_str = StringIO()
    headerList = []
    
    # Sort items
    reader = sorted(filter(reader, issue), key=itemgetter('Title'))
    
    if len(reader) > 0:
        file_str.write("<table width=600>")
        
    for row in reader:
        if (debug == 1):
            print row
        file_str.write("<tr>")
        
        file_str.write('<tr><td><a href="#toc_pub">TOC</a></td><td class="con-title"><a name="pub_' + str(len(headerList) + 1) + '">' + convert(row["Type of Publication"]) + ": " + convert(row["Title"]) + "</a></td></tr>\n")
        processTaggs(file_str,convert(row["Taggs"]))
        headerList.append(convert(row["Title"]))
        file_str.write('<tr class="odd"><td>' + "Journal/Publ." + "</td><td>" + convert(row["Journal"]) + "</td></tr>\n")
        file_str.write('<tr><td>' + "Abstract" + "</td><td>" + convert(row["Abstract"]) + "</td></tr>\n")
        file_str.write('<tr class="odd"><td>' + "Author/Editor" + "</td><td>" + convert(row["Authors/Editors"]) + "</td></tr>\n")
        file_str.write('<tr><td>' + "Information" + "</td><td>" + convert(row["Information"]) + "</td></tr>\n")
        file_str.write('<tr><td colspan=2><hr></td></tr>\n')
    
    if len(reader) > 0:
        file_str.write("</table>")
    
    subtoc(headerList, outfile, "pub")
    
    outfile.write(file_str.getvalue())
    outfile.close()
    print("Publications: Done.")