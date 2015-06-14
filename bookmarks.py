# -*- coding: UTF-8 -*-
import json
import urllib2

import os
import re
import database
from BeautifulSoup import BeautifulSoup
from flask import Flask, render_template, url_for, request, Response, flash
from werkzeug.utils import redirect

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'testowa.db'),
    DEBUG=True,
    SECRET_KEY='ddasdasuf0899012udjakl',
    USERNAME='admin',
    PASSWORD='default'
))
WRONG_URL_MSG = 'WRONG_URL'


@app.route('/')
def index():
    db = database.get_db()
    cur = db.execute("select id, title, url from Link")
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)


@app.route('/submit', methods=['POST'])
def submit():
    address = request.form['address']
    if len(address) > 0:
        if 'http://' not in address and 'https://' not in address:
            address = 'http://' + address
        try:
            req = urllib2.urlopen(address)
            doc = req.read()
            req.close()
            html = BeautifulSoup(doc)
            title = html.title.text
            title = re.search('^.{1,260}\\b', title if title else address).string
        except urllib2.URLError:
            flash(WRONG_URL_MSG, category='error')
            return redirect(url_for('index'))

        db = database.get_db()
        db.execute('insert into Link(title, url) values(?, ?)', [title, address])
        db.commit()
    return redirect(url_for('index'))


@app.route('/delete/all')
def delete():
    db = database.get_db()
    db.execute('delete from Link')
    db.execute('delete from Folder')
    db.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:link_id>', methods=['POST'])
def delete_link(link_id):
    database.delete_link(link_id)
    return Response(status=200)


def get_folder_tree(id=None, name=None):
    db = database.get_db()
    cur = db.execute(database.FOLDER_QUERY, {'id': id})
    result = {'name': name}
    children = {}
    for c in cur.fetchall():
        children[c['id']] = get_folder_tree(c['id'], c['name'])
    result['children'] = children
    return result if result else name


@app.route('/folders', methods=['GET'])
def folders():
    # tree = database.get_folder_tree()
    return render_template('foldery.html')


@app.route('/folders', methods=['POST'])
def folder_list():
    tree = database.get_folder_tree()
    resp = Response(status=200, mimetype='application/json')
    resp.set_data(json.dumps(tree, default=folder_encoder, encoding='UTF-8', ensure_ascii=False))
    return resp


def folder_encoder(fol):
    return fol.__dict__ if isinstance(fol, database.Folder) else fol


if __name__ == '__main__':
    app.run()
