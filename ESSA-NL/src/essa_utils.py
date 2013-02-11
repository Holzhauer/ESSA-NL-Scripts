'''
Utility functions

@author:  Sascha Holzhauer, CESR, Kassel, Germany
@date:    2011-04-21

History:  2011-04-11  (TOC, google download)
'''

import string 
import re
import cgi

from essa_config import *
import gdata.docs.service
import gdata.spreadsheet.service
import unicodedata

import htmlentitydefs as entity



# see http://code.google.com/intl/de-DE/apis/documents/docs/1.0/developers_guide_python.html#DownloadingSpreadsheets
def convert(text):
    if (text != None):
        if (replace_unicode_encode_error == 1):
            # unicodedata.normalize('NFKD', )
            text = convertURLs(unicode(text,'utf-8'))
            #unicode(convertURLs(text),'utf-8', 'replace')
        else:
            text = convertURLs(unicode(text,'utf-8'))
    else:
        text=""
    return text

# filter current issue
def filter(list, issue):
    new_list = []
    for item in list:
        if (item["Issue"] == issue):
            new_list.append(item)
    return new_list

# create TOC:
def subtoc(headerList, outfile, partShortName):    
    outfile.write('<a name="toc_' + partShortName + '"></a>')
    i = 0
    if len(headerList) > 0:
        outfile.write('<ol>')
        for header in headerList:
            i += 1
            outfile.write('<li><a href="#' + partShortName + '_' + str(i) + '">' + header + '</a></li>')
        outfile.write("</ol>\n")
    outfile.write('<a href="#content">Back to table of Contents</a><BR>\n')
    
# download spreadsheet from google as CVS
def downloadGoogleSpradsheet(partName, issue, workingDir, user, password):
    gd_client = gdata.docs.service.DocsService()
    gd_client.ClientLogin(user, password)
    
    spreadsheets_client = gdata.spreadsheet.service.SpreadsheetsService()
    spreadsheets_client.ClientLogin(user, password)

    # retrieve document by title    
    q = gdata.docs.service.DocumentQuery()
    q['title'] = 'ESSA_NL_' + partName
    q['title-exact'] = 'true'
    feed = gd_client.Query(q.ToUri())
    
    
    # substitute the spreadsheets token into our gd_client
    docs_auth_token = gd_client.GetClientLoginToken()
    gd_client.SetClientLoginToken(spreadsheets_client.GetClientLoginToken())

    file_path = workingDir + issue + "/ESSA_NL_" + partName + ".csv"
    print( 'Downloading spreadsheet to %s...' % (file_path,) )
    gd_client.Export(feed.entry[0], file_path)
    gd_client.SetClientLoginToken(docs_auth_token) # reset the DocList auth token


def checkURL(url):
#    p = urlparse(url)
#    h = HTTP(p[1])
#    h.putrequest('HEAD', p[2])
#    h.endheaders()
#    reply = h.getreply()[0]
#    if reply == 200:
#        return 1
#    else:
#        print "URL " + url + " does not exist! (" + str(reply) + ")"
#        return 1
    return 1

# convert URL-like text to HTML link
def convertURLs(text):
    if text != None:
        pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
        pat2 = re.compile(r"#(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
        result = ""
        words = []
        # substitute "DOI: " or "doi: " by http://dx.doi.org/
        text = string.replace(text, "DOI: ", "http://dx.doi.org/")
        text = string.replace(text, "doi: ", "http://dx.doi.org/")
        text = string.replace(text, "Doi: ", "http://dx.doi.org/")
        text = string.replace(text, "DOI:", "http://dx.doi.org/")
        text = string.replace(text, "doi:", "http://dx.doi.org/")
        text = string.replace(text, "Doi:", "http://dx.doi.org/")
        text = string.replace(text,u'\n'," <BR> ")
        for word in text.split():
            if (pat1.match(word) != None):
                if (checkURL(word)):                
                    word = pat1.sub(r'\1<a href="\2" target="_blank">\2</a>', word)
                    word = pat2.sub(r'\1<a href="http:/\2" target="_blank">\2</a>', word)
            elif word != "<BR>":
                # convert to HTML entities
                t = u''
                check = word
                for i in word:
                    if ord(i) in entity.codepoint2name:
                        name = entity.codepoint2name.get(ord(i))
                        t += "&" + name + ";"
                    else:
                        t += i
                word = t
            words.append(word)
        return string.join(words)

# Process item tags
def processTaggs(outfile, text):
    outfile.write('<tr><td colspan="2">')
    tags = ''
    if text.find("Policy") > -1:
        tags = tags + '<span class="policy">&nbsp;Policy&nbsp;</span>'
    if text.find("Market Dynamics") > -1:
        tags = tags + '<span class="marketDynamics">&nbsp;Market Dynamics&nbsp;</span>'
    if text.find("Reputation") > -1:
        tags = tags + '<span class="reputation">&nbsp;Reputation&nbsp;</span>'
    if text.find("Social Conflict") > -1:
        tags = tags + '<span class="socialConflict">&nbsp;Social Conflict&nbsp;</span>'
    if text.find("Social Networks") > -1:
        tags = tags + '<span class="socialNetworks">&nbsp;Social Networks&nbsp;</span>'
    if text.find("Societal Transition") > -1:
        tags = tags + '<span class="societalTransition">&nbsp;Societal Transition&nbsp;</span>'
    if text.find("ABM technical") > -1:
        tags = tags + '<span class="ABMtechnical">&nbsp;ABM technical&nbsp;</span>'
    if text.find("ABM methodical") > -1:
        tags = tags + '<span class="ABMmethodical">&nbsp;ABM methodical&nbsp;</span>'
    outfile.write(tags)
    outfile.write("</td></tr>")
