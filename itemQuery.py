import string
import requests
from dateutil.parser import parse
import xml.etree.ElementTree as ET

def runItems(feed):
    ''' =====================================================================================
        Returns a list of all the title of all items in the feed. Starts an HTTP session and 
        collects the raw text of the XML feed at the url.  Converts the rawtexts into an 
        element tree then makes a list of all the data from within the title tag of each item.
    
        feed: string representation of URL for RSS feed.
        
        Futurn Modifications: This function with soon return the date of the items 
        posted on the feed with the title.
    ''' 
    api_url = feed

    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    xml_data = raw_data.text
    root = ET.fromstring(xml_data)
    return getItems(root)

def getArticle(link):
    ''' =====================================================================================
        Returns the HTML of the article return from the link.  Starts an HTTP session to 
        query the url set to link.  Then returns the raw string of HTML returned from the
        request.
        
        link: article URL as a string
        
    '''
    api_url = link

    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    return raw_data.text

def getTitle(item):
    ''' =====================================================================================
        Takes in a item tree element from the document tree of an RSS feed and returns the 
        title of the item
        
        item: Item Element Tree Node    
    
    '''
    for child in item:
        if child.tag == 'title':
            return child.text

def getItems(root):
    ''' =====================================================================================
        Returns a list of item element tree nodes under the root node of a element tree for
        an RSS feed.
        
        root: is the element tree of a XML document representing an RSS feed of
        "item" tags
    
    
    '''
    itemRecords = []
    for child in root:
        if child.tag == 'item':
            itemRecords.append(getTitle(child))
        else:
            itemRecords.extend(getItems(child))
    return itemRecords

def findContent(articlePage, elmTag):
    ''' =====================================================================================
        Returns the HTML string of the protion of the document articlePage within the element
        tag elmtag.  The start tag with atributes is matched to elmTag, divs are counted and 
        matched to closing tags to find the closing tag of the element when found
        
        articlPage:  The full HTML article page as a string
        elmTag: Starting tag of desired element as a string (example: '<div class="article-content">')
        
        Assumptions: The desired elmTag is a 'div' tag
        Future Modifictions:  This function along with other document filters will be writen
        as extentions to pythons HTMLparser class.
    
    
    '''
    offs = len(elmTag)
    for i in range(len(articlePage)):
        if articlePage[i:i+offs] == elmTag:
            #print("found" + elmTag)
            break
    contentA = articlePage[i:]
    
    divs = 0
    openTag = '<div' # Length is + 4 for open Tag
    closeTag = '</div>' # Legnth is + 6 for closing Tag
    
    ## Now count the divs and their closing tags
    for j in range(len(contentA)):
        if contentA[j:j+4] == openTag:
            divs += 1
        if contentA[j:j+6] == closeTag:
            divs -= 1
            if divs == 0:
                return contentA[:j+6]

