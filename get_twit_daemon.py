import tweepy
import sys
import psycopg2
import my_db
import re
from word_list import words


# Twitter credential
consumer_key = 'd5qhU69TNYmuT608SPk7Wy5VZ'
consumer_secret = 'QuJziBDzwwss8P5WatwdZigCvhB5r2tphRbvWGOaKZ3RcY1cil'
access_token = '3019121609-3U2LQvT4XNYuWeX0SkSW7WdKhQlnF5JqP9lIemh'
access_token_secret = '3Q9jVLQaULyu2Kj0QEYgxzVvqURYZetTl1naOCi6ycxZl'
# Database connection
conn = None
cur = None
# splitter function
splitter = re.compile(r'\W+')
# keyword set
keywords = set(words)


def clean_old_records(p_conn, p_cur):
    count_sql = '''
    SELECT count(*) FROM twit;
    '''
    clean_sql = '''
    DELETE FROM twit
    WHERE twit_id IN (
    SELECT twit_id FROM twit
    ORDER BY twit_id DESC OFFSET 1000
    );
    '''
    p_cur.execute(count_sql)
    num = p_cur.fetchone()
    if num[0] <= 2000:
        return
    p_cur.execute(clean_sql)
    p_conn.commit()


def add_new_record(p_conn, p_cur, longitude, latitude, text):
    sql_base = '''
    INSERT INTO twit (longitude,latitude,words) VALUES (%d, %d, '%s');
    '''
    sql = sql_base % (longitude, latitude, text)
    # print sql.strip()
    p_cur.execute(sql)
    p_conn.commit()


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if not status.coordinates:
            return
        global splitter, keywords
        longitude, latitude = status.coordinates['coordinates']
        text = status.text.encode('utf-8').lower()
        words = filter(bool, splitter.split(text))
        text = ' '.join(words)
        if not [x for x in words if x in keywords]:
            return
        global conn, cur
        clean_old_records(conn, cur)
        add_new_record(conn, cur, longitude, latitude, text)

    def on_error(self, status_code):
        print >> sys.stderr, 'Error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


def main():
    global conn, cur
    conn = psycopg2.connect(
        host=my_db.hostname,
        dbname=my_db.dbname,
        user=my_db.user,
        password=my_db.paswd
    )
    cur = conn.cursor()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
    sapi.filter(locations=[-130, -60, 70, 60])


'''
Usage:
python get_twit_daemon.py
'''
if __name__ == '__main__':
    main()
