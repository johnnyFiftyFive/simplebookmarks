from bookmarks import app
from sqlite3 import dbapi2 as sqlite3
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

def get_folder_tree(id=None, name=None):
    db = get_db()
    cur = db.execute(FOLDER_QUERY, {'id': id})
    result = {'name': name}
    children = {}
    for c in cur.fetchall():
        children[c['id']] = get_folder_tree(c['id'], c['name'])
    result['children'] = children
    return result if result else name

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()