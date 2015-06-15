import json
from sqlite3 import dbapi2 as sqlite3

from bookmarks import app
from flask import g

DELETE_LINK_QUERY = 'DELETE FROM Link WHERE id = :id'
FOLDER_QUERY = 'SELECT id, name, parent FROM Folder WHERE parent is :id'
UPDATE_LINK_QUERY = 'UPDATE Link SET title=:title, url=:url WHERE id=:id'

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


def get_folder_tree(id=None):
    db = get_db()
    cur = db.execute(FOLDER_QUERY, {'id': id})
    folders = []
    for c in cur.fetchall():
        folder = Folder(c['id'], c['name'])
        folder.children = get_folder_tree(c['id'])
        folders.append(folder)
    return folders


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


class Folder:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        self.children = []

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


def delete_link(link_id):
    db = get_db()
    db.execute(DELETE_LINK_QUERY, {'id': link_id})
    db.commit()
    return


def update(data):
    db = get_db()
    items = db.execute(UPDATE_LINK_QUERY, (data['title'], data['url'], data['id']))
    db.commit()
    return items.rowcount
