'''
Download, format and store job offer items

@author:  Sascha Holzhauer, CESR, Kassel, Germany
@date:    2011-04-21

History:  2011-04-11  (TOC, sorting, google download)
'''

import csv
from operator import itemgetter
#from cStringIO import StringIO
from io import StringIO
 
from essa_utils import *

def format(outputFile, issue, workingDir, user, password, debug, chapNum):
    
    # download as CVS to working dir
    downloadGoogleSpradsheet("Jobs", issue, workingDir, user, password)
    
    inputFile = workingDir + issue + "/ESSA_NL_Jobs.csv"
    
    reader = csv.DictReader(open(inputFile, 'rb'), delimiter=',', quotechar='"')
    
    outfile = open(outputFile, 'a')
    
    
    outfile.write('\n\n<h1><a name="jobs">' + str(chapNum) + '. Job Offers</a></h1>')
    outfile.write('<p>Note: Job offers are ordered according to job type.</p>\n')
    
    file_str = StringIO()
    headerList = []
    
    # Sort items
    reader = sorted(filter(reader, issue), key=itemgetter('Job Type'))

    if len(reader) > 0:
        file_str.write("<table width=600>")

    for row in reader:
        if (debug == 1):
            print( row )
        file_str.write("<tr>")
        file_str.write('<tr><td><a href="#toc_job">TOC</a></td><td class="con-title"><a name="job_' + str(len(headerList) + 1) + '">' + convert(row["Job Type"]) + ": " + convert(row["Title"]) + "</a></td></tr>")
        processTaggs(file_str, convert(row["Taggs"]))
        headerList.append(convert(row["Job Type"]) + ": " + convert(row["Title"]))
        file_str.write('<tr  class="odd"><td>Place</td><td>' + convert(row["Place"]) + "</td></tr>")
        file_str.write('<tr><td>Organisation</td><td>' + convert(row["Organisation"]) + "</td></tr>")
        file_str.write('<tr  class="odd"><td>Requirements</td><td>' + convert(row["Requirements"]) + "</td></tr>")
        file_str.write('<tr><td>Description</td><td>' + convert(row["Description"]) + "</td></tr>")
        file_str.write('<tr  class="odd"><td>Salary</td><td>' + convert(row["Salary"]) + "</td></tr>")
        file_str.write('<tr><td>Contact</td><td>' + convert(row["Contact"]) + "</td></tr>")
        file_str.write('<tr  class="odd"><td>Application Deadline</td><td>' + convert(row["Application deadline"]) + "</td></tr>")
        if (row["Further Information"] != "" and row["Further Information"] != None):
            file_str.write('<tr><td>Further Information</td><td>' + convert(row["Further Information"]) + "</td></tr>")
        
                   
        file_str.write("</tr>")
        file_str.write("<tr><td colspan=2><hr></td></tr>")
    
    if len(reader) > 0:
        file_str.write("</table>")
    
    subtoc(headerList, outfile, "job")
    
    outfile.write(file_str.getvalue())
    outfile.close()
    print("Jobs: Done.")
