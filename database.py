from sqlite3 import dbapi2 as sqlite3

from bookmarks import app
from flask import g

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
