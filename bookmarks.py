import json
import urllib2
from sqlite3 import dbapi2 as sqlite3

import os
import re
from BeautifulSoup import BeautifulSoup
from flask import Flask, render_template, g, url_for, request
from werkzeug.utils import redirect

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'testowa.db'),
    DEBUG=True,
    SECRET_KEY='ddasdasuf0899012udjakl',
    USERNAME='admin',
    PASSWORD='default'
))

FOLDER_QUERY = "SELECT id, name, parent FROM Folder WHERE parent is :id"

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# # # # # # # # # # # # # # # # # # # # # # # # # #

@app.route('/')
def index():
    db = get_db()
    cur = db.execute("select title, url from Link")
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/submit', methods=['POST'])
def submit():
    address = request.form['address']
    if len(address) > 0:
        if 'http://' not in address and 'https://' not in address:
            address = 'http://' + address

        req = urllib2.urlopen(address)

        doc = req.read()
        req.close()
        html = BeautifulSoup(doc)
        title = html.title.text
        title = re.search('^.{1,260}\\b', title if title else address).string

        db = get_db()
        db.execute('insert into Link(title, url) values(?, ?)', [title, address])
        db.commit()

    return redirect(url_for('index'))

@app.route('/delete')
def delete():
    db = get_db()
    db.execute('delete from Link')
    db.execute('delete from Folder')
    db.commit()
    return redirect(url_for('index'))

def get_folder_tree(id=None, name=None):
    db = get_db()
    cur = db.execute(FOLDER_QUERY, {'id': id})
    result = {'name': name}
    children = {}
    for c in cur.fetchall():
        children[c['id']] = get_folder_tree(c['id'], c['name'])
    result['children'] = children
    return result if result else name

@app.route('/folders')
def folders():
    tree = get_folder_tree()['children']
    return json.dumps(tree, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
