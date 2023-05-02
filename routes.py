#http://127.0.0.1:5000
from flask import Flask, render_template
import sqlite3

app=Flask(__name__)

def retrieve(query,parameters):
    conn = sqlite3.connect('notes_app.db')
    cur = conn.cursor()
    cur.execute(query,parameters)
    return(cur.fetchall())

#try get a retrieve function which incorporates both parameters and no parameters
def retrievenop(query):
    conn = sqlite3.connect('notes_app.db')
    cur = conn.cursor()
    cur.execute(query)
    return(cur.fetchall())

@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/all-subjects')
def subjects():
    subjects = retrievenop('SELECT id, name FROM SUBJECT')
    return render_template('pages/subjects.html',subjects=subjects)


@app.route('/subject/<int:id>')
def subject(id):
    infoname = retrieve("SELECT info, name FROM SUBJECT WHERE id = ?", (id,))
    categories = retrieve("SELECT id, name FROM CATEGORY WHERE subject_id = ?", (id,))
    return render_template('pages/subject.html',infoname=infoname,categories=categories)


@app.route('/category/<int:id>')
def category(id):
    infoname = retrieve("SELECT name, info FROM CATEGORY WHERE id = ?", (id,))
    entries = retrieve("SELECT id, name FROM ENTRY WHERE category_id = ?", (id,))
    return render_template('pages/category.html',infoname=infoname,entries=entries)


@app.route('/entry/<int:id>')
def entry(id):
    information = retrieve("SELECT name, entry FROM ENTRY WHERE id = ?",(id,))
    tags = retrieve("SELECT id, name FROM ENTRYTAG\nJOIN TAG ON TAG.id = tag_id\nWHERE entry_id = ?",(id,))
    return render_template('pages/entry.html',information=information,tags=tags)


@app.route('/create-entry')
def create():
    tags = retrievenop('SELECT id, name FROM TAG')
    return render_template('pages/create.html',tags=tags)


@app.route('/all-tags')
def tags():
    tags = retrievenop('SELECT id, name FROM TAG')
    return render_template('pages/tags.html',tags=tags)


@app.route('/tag/<int:id>')
def tag(id):
    infoname = retrieve('SELECT name, info FROM TAG WHERE id = ?',(id,))
    entries = retrieve('SELECT id, name FROM ENTRYTAG\nJOIN ENTRY ON ENTRY.id = entry_id\nWHERE tag_id = ?',(id,))
    return render_template('pages/tag.html',infoname=infoname,entries=entries)


@app.route('/create-tag')
def create_tag():
    return render_template('pages/create_tag.html')


if __name__=='__main__':
    app.run(debug=True)