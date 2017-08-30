from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        for attr in attrs:
            print(attr, end= ' ')
        print(' ')

    #def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)

    #def handle_data(self, data):
        #print("Encountered some data  :", data)

class articleContentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.articleContent = ''
        self.articleContentDiv = False
        self.script = False
        self.twitterContent = False
        self.divs = 0
        self.scripts = 0
        self.posts = 0
    
    def handle_starttag(self, tag, attrs):        
        if tag == 'div':
            if ('class', 'article-content') in attrs:
                self.articleContentDiv = True
               #print("ContentOn")
        
        if self.articleContentDiv and tag == 'div':
            self.divs += 1
        
        if tag == 'script':
            self.script = True
            self.scripts += 1
            #print("scriptOn")
            
        if tag == 'blockquote':                  
            self.twitterContent = True
            self.posts += 1
            #print("TwitterOn")

    def handle_endtag(self, tag):
        if self.articleContentDiv and tag == 'div':
            self.divs -= 1
            if self.divs == 0:
                self.articleContentDiv = False
                #print("ContentOff")
                
        if tag == 'script':
            self.script = False
            #print("scriptOFF")
            
        if tag == 'blockquote':
            self.twitterContent = False
            #print("TwitterOFF")
            
        if tag == 'html':
            print('ARTICLE: Scripts ' + str(self.scripts) + '     Detected Posts ' + str(self.posts))

    def handle_data(self, data):
        #print("Encountered some data  :", data)
        if self.articleContentDiv and not (self.script or self.twitterContent):
            self.articleContent += data
            self.articleContent += ' '
    
    def getContent(self):
        return self.articleContent

class paneContentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.articleContent = ''
        self.articleContentDiv = False
        self.script = False
        self.scripts = 0
        self.twitterContent = False
        self.divs = 0
        self.scripts = 0
        self.posts = 0
    
    def handle_starttag(self, tag, attrs):        
        if tag == 'div':
            if ('class', 'pane-content') in attrs:
                self.articleContentDiv = True
                #print("PaneOn")
        
        if self.articleContentDiv and tag == 'div':
            self.divs += 1
        
        if tag == 'script':
            self.script = True
            self.scripts += 1
           # print("scriptOn")
            
        if tag == 'blockquote':                  
            self.twitterContent = True
            self.posts += 1
            #print("TwitterOn")

    def handle_endtag(self, tag):
        if self.articleContentDiv and tag == 'div':
            self.divs -= 1
            if self.divs == 0:
                self.articleContentDiv = False
                #print("PaneOff")
                
        if tag == 'script':
            self.script = False
            #print("scriptOFF")
            
        if tag == 'blockquote':
            self.twitterContent = False
            #print("TwitterOFF")
        
        if tag == 'html':
            print('PANE:    Scripts ' + str(self.scripts) + '     Detected Posts ' + str(self.posts))

    def handle_data(self, data):
        #print("Encountered some data  :", data)
        if self.articleContentDiv and not (self.script or self.twitterContent):
            self.articleContent += data
            self.articleContent += ' '
    
    def getContent(self):
        return self.articleContent