import string
import requests
from dateutil.parser import parse
import xml.etree.ElementTree as ET

def recordsFromFeed(teamNewsFeedLink):
    ''' =====================================================================================
        Returns a list of all the title of all items in the feed. Starts an HTTP session and 
        collects the raw text of the XML feed at the url.  Converts the rawtexts into an 
        element tree then makes a list of all the data from within the title tag of each item.
    
        feed: string representation of URL for RSS feed.
        
        Futurn Modifications: This function with soon return the date of the items 
        posted on the feed with the title.
        
        MODIFED FROM: runItems(root)
    ''' 
    api_url = teamNewsFeedLink

    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    xml_data = raw_data.text
    #try:
    root = ET.fromstring(xml_data)
    #except ET.ParseError:
        #print("There is a Parse Error Here")
        #return ['','','','null','']
    return getFeedRecords(root)

def teamNews(teamNewsFeedLink):
    ''' =====================================================================================
        Returns a list of all the title of all items in the feed. Starts an HTTP session and 
        collects the raw text of the XML feed at the url.  Converts the rawtexts into an 
        element tree then makes a list of all the data from within the title tag of each item.
    
        feed: string representation of URL for RSS feed.
        
        Futurn Modifications: This function with soon return the date of the items 
        posted on the feed with the title.
        
        MODIFED FROM: runItems(root)
    ''' 
    api_url = teamNewsFeedLink

    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    xml_data = raw_data.text
    root = ET.fromstring(xml_data)
    return getFeedSummary(root)

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
        
def getLink(item):
    ''' =====================================================================================
        Takes in a item tree element from the document tree of an RSS feed and returns the 
        link to the article for the item
        
        item: Item Element Tree Node    
    
    '''
    for child in item:
        if child.tag == 'link':
            return child.text
        
def getDate(item):
    ''' =====================================================================================
        Takes in a item tree element from the document tree of an RSS feed and returns the 
        date and time the item was posted
        
        item: Item Element Tree Node    
    
    '''
    for child in item:
        if child.tag == 'pubDate':
            return child.text
        
def getDiscription(item):
    ''' =====================================================================================
        Takes in a item tree element from the document tree of an RSS feed and returns the 
        date and time the item was posted
        
        item: Item Element Tree Node    
    
    '''
    for child in item:
        if child.tag == 'description':
            return child.text
        
def getCreator(item):
    ''' =====================================================================================
        Takes in a item tree element from the document tree of an RSS feed and returns the 
        date and time the item was posted
        
        item: Item Element Tree Node    
    
    '''
    for child in item:
        if child.tag == '{http://purl.org/dc/elements/1.1/}creator':
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

def getItemTitles(root):
    ''' =====================================================================================
        Returns a list of item element tree nodes under the root node of a element tree for
        an RSS feed.
               
        root: is the element tree of a XML document representing an RSS feed of
        "item" tags
    
        MODIFIED FROM: getItems(root)
    '''
    itemRecords = []
    for child in root:
        if child.tag == 'item':
            itemRecords.append(getTitle(child))
        else:
            itemRecords.extend(getItemTitles(child))
    return itemRecords

def getItemLinks(root):
    ''' =====================================================================================
        Returns a list of item element tree nodes under the root node of a element tree for
        an RSS feed.
        
        root: is the element tree of a XML document representing an RSS feed of
        "item" tags
    
        MODIFIED FROM: getItems(root)
    '''
    itemRecords = []
    for child in root:
        if child.tag == 'item':
            itemRecords.append(getLink(child))
        else:
            itemRecords.extend(getItemLinks(child))
    return itemRecords

def getItemDates(root):
    ''' =====================================================================================
        Returns a list of item element tree nodes under the root node of a element tree for
        an RSS feed.
        
        root: is the element tree of a XML document representing an RSS feed of
        "item" tags
    
        MODIFIED FROM: getItems(root)
    '''
    itemRecords = []
    for child in root:
        if child.tag == 'item':
            itemRecords.append(getDate(child))
        else:
            itemRecords.extend(getItemDates(child))
    return itemRecords

def getTitleLinks(root):
    ''' =====================================================================================
        Returns the title and link for each item in the RSS feed element tree as a list of 
        tupled pairs.
        
        root: is the element tree of a XML document representing an RSS feed of
        "item" tags
    
        MODIFIED FROM: getItems(root)
    '''
    itemRecords = []
    for child in root:
        if child.tag == 'item':
            itemRecords.append((getTitle(child), getLink(child)))
        else:
            itemRecords.extend(getTitleLinks(child))
    return itemRecords

def getFeedRecords(root):
    ''' =====================================================================================
        Returns the a list of tuples that sumarize the items of a RSS feed element tree. Each
        tuple is for a single item and comprises 0: the title of the item, 1: the time the 
        item was published and 2: the link to the article for the item.
        
        root: is the element tree of a XML document representing an RSS feed of
        "item" tags
    
        MODIFIED FROM: getItems(root)
    '''
    itemRecords = []
    for child in root:
        if child.tag == 'item':
            itemRecords.append((getDate(child), getTitle(child), getLink(child), getDiscription(child), getCreator(child)))
        else:
            itemRecords.extend(getFeedRecords(child))
    return itemRecords

def getFeedSummary(root):
    ''' =====================================================================================
        Returns the a list of tuples that sumarize the items of a RSS feed element tree. Each
        tuple is for a single item and comprises 0: the title of the item, 1: the time the 
        item was published and 2: the link to the article for the item.
        
        root: is the element tree of a XML document representing an RSS feed of
        "item" tags
    
        MODIFIED FROM: getItems(root)
    '''
    itemRecords = []
    for child in root:
        if child.tag == 'item':
            itemRecords.append((getTitle(child), getDate(child), getLink(child)))
        else:
            itemRecords.extend(getFeedSummary(child))
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

