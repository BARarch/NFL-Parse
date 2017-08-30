import itemQuery as iq
import articleParse as ap
from string import ascii_letters, digits

def ExtractAlphanumeric(InputString):
    return "".join([ch for ch in InputString if ch in (ascii_letters + digits + ' ' )])

def parseForCorpus(link):
    article = iq.getArticle(link)
    
    articleParser = ap.articleContentParser()
    articleParser.feed(article)
    article1 = articleParser.getContent()
    
    if not article1:
        # switch to pane parseing
        paneParser = ap.paneContentParser()
        paneParser.feed(article)
        article1 = paneParser.getContent()
    
    # Alpha Numeric Cleaning
    clean1 = ExtractAlphanumeric(article1)
    
    sp1 = clean1.split(' ')
    
    # Space and Link Cleaning
    sp2 = [elm for elm in sp1 if elm] # Spaces Longer than one character
    sp3 = [elm for elm in sp2 if 'http' not in elm] # No links
    noWords = len(sp3)
    
    clean2 = ' '.join(sp3)
    
    return clean2, noWords
        