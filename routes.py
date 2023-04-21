from flask import Flask, render_template
import sqlite3

app=Flask(__name__)


@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/all-subjects')
def subjects():
    return render_template('pages/subjects.html')


@app.route('/subject/<int:id>')
def subject():
    return render_template('pages/subject.html')


@app.route('/category/<int:id>')
def category():
    return render_template('pages/category.html')


@app.route('/entry<int:id>')
def entry():
    return render_template('pages/entry.html')


@app.route('/create-entry')
def create():
    return render_template('pages/create.html')


@app.route('/all-tags')
def tags():
    return render_template('pages/tags.html')


@app.route('/tag/<int:id>')
def tag():
    return render_template('pages/tag.html')


@app.route('/create-tag')
def create_tag():
    return render_template('pages/creat_tag.html')


if __name__=='__main__':
    app.run(debug=True)