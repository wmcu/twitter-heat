from flask import Flask, jsonify, render_template, request, url_for
import psycopg2
import subprocess
import my_db
import sys
import os
from word_list import words


# Create an Flask app object.  We'll use this to create the routes.
application = app = Flask(__name__)
app.config['DEBUG'] = True


#MY_URL = r'http://localhost:5000'

# Database connection
conn = None
cur = None

@app.before_first_request
def init():
    # connect database
    global conn, cur
    conn = psycopg2.connect(
        host=my_db.hostname,
        dbname=my_db.dbname,
        user=my_db.user,
        password=my_db.paswd
    )
    cur = conn.cursor()

# main pages
@app.route('/')
def index():
    # load keywords
    payload = {'keywords': words}
    return render_template('index.html', api_data=payload)


@app.route('/data/<word>')
def search(word):
    global conn, cur
    sql = r'SELECT longitude, latitude, words FROM twit ORDER BY twit_id DESC LIMIT 500;'
    result = []
    cur.execute(sql)
    for record in cur:
        if word == '-ALL-' or word in record[2].split():
            result.append({'longitude': record[0], 'latitude': record[1]})
    return jsonify({'data': result})


# Internal helper
@app.route('/insert/<longitude>/<latitude>/<word>')
def insert_db(longitude, latitude, word):
    global conn, cur
    words = word.split('+')
    text = ' '.join(words)
    sql_base = '''
    INSERT INTO twit (longitude,latitude,words) VALUES (%s, %s, '%s');
    '''
    sql = sql_base % (longitude, latitude, text)
    result = []
    cur.execute(sql)
    conn.commit()
    return 'success'


# Error Handler
@app.errorhandler(404)
def not_found(error):
    return 'Page Not Found', 404


@app.errorhandler(500)
def internal_server_error(error):
    return 'Internal Server Error', 500


# If the user executed this python file (typed `python app.py` in their
# terminal), run our app.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
