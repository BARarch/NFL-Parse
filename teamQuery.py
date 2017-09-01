import psycopg2
import config as config

conn = config.connect()
cursor = conn.cursor()

teamList = [
    "Ravens",
    "Steelers",
    "Browns",
    "Bengals",
    "Vikings",
    "Lions",
    "Packers",
    "Patriots",
    "Jets",
    "Bills",
    "Dolphins",
    "Redskins",
    "Giants",
    "Eagles",
    "Cowboys",
    "Jaguars",
    "Colts",
    "Titans",
    "Texans",
    "Panthers",
    "Saints",
    "Falcons",
    "Buccaneers",
    "Raiders",
    "Chiefs",
    "Broncos",
    "Seahawks",
    "49ers",
    "Cardinals",
    "Rams"           
]

def teamQueryCounts(team):
    conn = config.connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT news_corpus.id, link, team, type, date, word_count FROM news_corpus INNER JOIN team_articles ON team_articles.id = news_corpus.article_id WHERE team = '%s'" % team)
    
    elms = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return elms

def teamQueryTexts(team):
    conn = config.connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT news_corpus.id, link, team, article_text FROM news_corpus INNER JOIN team_articles ON team_articles.id = news_corpus.article_id WHERE team = '%s'" % team)
    
    elms = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return elms