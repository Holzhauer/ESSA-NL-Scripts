'''
Download, format and store Conference - CfParticipation items

@author:  Sascha Holzhauer, CESR, Kassel, Germany
@date:    2011-04-21

History:  2011-04-11  (TOC, sorting, google download)

TODO
- check for registration deadline in future

'''

import csv
from operator import itemgetter
from essa_utils import *
from cStringIO import StringIO

def format(outputFile, issue, workingDir, user, password, debug, chapNum):

    # download as CVS to working dir
    downloadGoogleSpradsheet("Participation", issue, workingDir, user, password)

    inputFile = workingDir + issue + "/ESSA_NL_Participation.csv"
    
    reader = csv.DictReader(open(inputFile, 'rb'), delimiter=',', quotechar='"')
    
    outfile = open(outputFile, 'a')
    
    outfile.write('\n\n<h1><a name="CfA">' + str(chapNum) + '. Calls for Attendance for Conferences, Workshops, Meetings and Symposia</a></h1>')
    outfile.write('<p>Note: CfAs are ordered according to their title.</p>\n')
    
    file_str = StringIO()
    
    headerList = []
    
    # Sort items
    reader = sorted(filter(reader, issue), key=itemgetter('Title'))
    
    if len(reader) > 0:
        file_str.write("<table width=600>")
    for row in reader:
        if (debug == 1):
            print row
        outfile.write("<tr>")
        if (row["Short Title"] != "" and row["Short Title"] != None and row["Short Title"] != "-"):
            shortTitle = convert(row["Short Title"]) + ": "
        else:
            shortTitle = ""
        headerList.append(shortTitle + convert(row["Title"]))
        file_str.write('<tr><td><a href="#toc_att">TOC</a></td><td class="con-title"><a name="con_' + str(len(headerList) + 1) + '">' + shortTitle + convert(row["Title"]) + "</a></td></tr>\n")
        processTaggs( file_str, convert(row["Taggs"]))
        file_str.write('<tr class="odd"><td>Date</td><td>' + convert(row["Date"]) + "</td></tr>\n")
        file_str.write('<tr><td>Place</td><td>' + convert(row["Place"]) + "</td></tr>\n")
        file_str.write('<tr class="odd"><td>Organisation</td><td>' + convert(row["Organisation"]) + "</td></tr>\n")
        file_str.write('<tr><td>Registration Deadline</td><td>' + convert(row["Registration Deadline"]) + "</td></tr>\n")
        file_str.write('<tr class="odd"><td>Topics</td><td>' + convert(row["Topics"]) + "</td></tr>\n")
        file_str.write('<tr><td>Website</td><td>' + convert(row["Website"]) + "</td></tr>\n")                   
        file_str.write("</tr>\n")
        file_str.write("<tr><td colspan=2><hr></td></tr>\n\n")
        
    if len(reader) > 0:
        file_str.write("</table>")
    
    subtoc(headerList, outfile, "att")
    outfile.write(file_str.getvalue())
    outfile.close()
    print("Conference Attendance: Done.")