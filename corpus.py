import psycopg2
import config as config
import cleaner as cl
import requests.exceptions as RE

newsFeedTypes = ['News', 'All News', 'news', 'TeamNews', 'Latest Content', 'News Stories', 'Team Stories', 'Latest Headlines', 'Articles']
newsTypeConditions = 'type = ' + " OR type = ".join(["\'" + t + "\'" for t in newsFeedTypes])

def pushCorpus(links):
    '''
        For each link 
        1) extract article text
        2) clean it
        3) push the text the word count and the foreign key to news_corpus table
    '''
    
    conn = config.connect()
    cursor = conn.cursor()
    pushedElms = 0
    
    for elm in links:
        try:
            link = elm[1]
            clean = cl.parseForCorpus(link)
            cursor.execute(
            "INSERT INTO news_corpus (article_text, word_count, article_id) VALUES (%s, %s, %s);",
            (clean[0], clean[1], elm[0]))
            pushedElms += 1
        except RE.RequestException:
            print("Request Exception Caught from " + link)
     
    conn.commit()
    print(str(pushedElms) + " new records intserted into news_corpus")
    
    cursor.close()
    conn.close()
    
    return pushedElms

def corpusAllArticles():
    '''
        Pushes all records from the team_news table to the corpus
    '''
    conn = config.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, link, date FROM team_articles WHERE %s" % newsTypeConditions)
    newsLinks = (cursor.fetchall())
    cursor.close()
    conn.close()
    
    return pushCorpus(newsLinks)

def corpusNewArticles():
    '''
        Finds new articles in the team_articles table that have not been corpused
        and corpuses them
    '''
    conn = config.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT article_id from news_corpus order by id desc limit 1");
    lastId = cursor.fetchall()[0][0]
    print('lastId:' + str(lastId))

    cursor.execute("SELECT id, link, date FROM team_articles WHERE (id > %s) AND (%s)" % (lastId,newsTypeConditions))
    newsLinks = (cursor.fetchall())
    #print (newsLinks)

    cursor.close()
    conn.close()
    
    return pushCorpus(newsLinks)

def dbSize():
    conn = config.connect()
    cursor = conn.cursor()

    cursor.execute(" SELECT pg_size_pretty( pg_database_size('nflparse'))")
    dbsize = cursor.fetchall()[0][0]

    cursor.execute(" SELECT pg_size_pretty( pg_total_relation_size('news_corpus'))")
    corpusSize = cursor.fetchall()[0][0]

    cursor.close()
    conn.close()

    return dbsize, corpusSize
    