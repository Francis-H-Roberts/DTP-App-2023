#http://127.0.0.1:5000
from flask import Flask, render_template
from flask import request
import sqlite3

app=Flask(__name__)

#basic function for retrieval of information with parameters
def retrieve(query,parameters):
    conn = sqlite3.connect('notes_app.db')
    cur = conn.cursor()
    cur.execute(query,parameters)
    results = cur.fetchall()
    conn.commit()
    return(results)


#try get a retrieve function which does incorporates the function of this one and retrieve
#retrieve with no parameters
def retrievenop(query):
    conn = sqlite3.connect('notes_app.db')
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    return(results)


#function to insert data into db 
def insert(query,parameters):
    conn = sqlite3.connect('notes_app.db')
    cur = conn.cursor()
    cur.execute(query,parameters)
    conn.commit()
    return


def enter_tags(id):
    #A rather convoluted method of obtaining the selected tags and inserting them (fix later)
    #Got the keys bit from https://stackoverflow.com/questions/58160006/how-to-get-multiple-elements-from-a-form-using-request-form-get
    keys = request.form.keys()
    tags = []
    for key in keys:
        if key!='name' and key!='entry': 
            tags.append(request.form.get(key))
    for tag in tags:
        insert("INSERT INTO ENTRYTAG(tag_id,entry_id) VALUES (?,?)",(tag,id))


#home not a whole lot going on atm
@app.route('/')
def home():
    return render_template('pages/home.html')


#displays the contents of the root folder
@app.route('/main-directory')
def root():
    folders = retrievenop('SELECT id, name FROM FOLDER WHERE parent_id = 1')
    entries = retrievenop('SELECT id, name FROM ENTRY WHERE parent_id = 1')
    return render_template('pages/root.html',folders=folders,entries=entries,id=1)


#displays the folders/entries within the folder with its id in the route
@app.route('/folder/<int:id>')
def folder(id):
    infoname = retrieve("SELECT name,info FROM FOLDER WHERE id = ?", (id,))[0]
    folders = retrieve("SELECT id, name FROM FOLDER WHERE parent_id = ?", (id,))
    entries = retrieve("SELECT id, name FROM ENTRY WHERE parent_id = ?", (id,))
    return render_template('pages/folder.html',infoname=infoname,folders=folders,entries=entries,id=id)


@app.route('/create-folder/<int:id>')
def create_folder(id):
    parents = retrievenop("SELECT id, name FROM FOLDER")
    return render_template('pages/create_folder.html',id=id,parents=parents)


@app.route('/create-folder/<int:id>',methods=["POST"])
def folder_created(id): 
    name = request.form.get('name')
    info = request.form.get('entry')
    insert("INSERT INTO FOLDER(parent_id,name,info) VALUES (?,?,?)",(id,name,info))
    return render_template('pages/home.html')


@app.route('/edit-folder/<int:id>')
def edit_folder(id):
    info = retrieve("SELECT parent_id,name,info FROM FOLDER WHERE id = ?",(id,))[0]
    folders = retrievenop('SELECT id, name FROM FOLDER')
    return render_template('pages/edit_folder.html',info=info,parents=folders)


@app.route('/edit-folder/<int:id>',methods=["POST"])
def folder_edited(id):
    parent_id = request.form.get('parent')
    name = request.form.get('name')
    info = request.form.get('entry')
    insert("UPDATE FOLDER SET (parent_id,name,info) = (?,?,?) WHERE id = ?",(parent_id,name,info,id))
    return render_template('pages/home.html')


#displays the entry that has its id in the route
@app.route('/entry/<int:id>')
def entry(id):
    information = retrieve("SELECT name, entry FROM ENTRY WHERE id = ?",(id,))
    tags = retrieve("SELECT id, name FROM ENTRYTAG\nJOIN TAG ON TAG.id = tag_id\nWHERE entry_id = ?",(id,))
    return render_template('pages/entry.html',information=information,tags=tags,id=id)


#displays a form with the parameters for an entry
@app.route('/create-entry/<int:id>')
def create_entry(id):
    tags = retrievenop('SELECT id, name FROM TAG')
    folders = retrievenop('SELECT id, name FROM FOLDER')
    return render_template('pages/create.html',tags=tags,id=id,folders=folders)


#I gained my understanding of forms from https://discuss.codecademy.com/t/what-happens-after-submit-is-pressed-where-does-the-information-go/478914/2
#and how they work in flask from https://plainenglish.io/blog/how-to-create-a-basic-form-in-python-flask-af966ee493fa
@app.route('/create-entry/<int:id>',methods=["POST"])
def entry_creation(id):  
    name = request.form.get('name')
    entry = request.form.get('entry')
    id = request.form.get('folder')
    insert("INSERT INTO ENTRY(parent_id,name,entry) VALUES (?,?,?)",(id,name,entry))
    enter_tags(max(retrievenop("SELECT id FROM ENTRY"))[0])
    return render_template('pages/home.html')


#A page that provides a form for editing an existing entry
@app.route('/edit-entry/<int:id>')
def edit_entry(id):
    information = retrieve("SELECT parent_id, name, entry FROM ENTRY WHERE id = ?",(id,))[0]
    tags = retrieve("SELECT id, name FROM ENTRYTAG\nJOIN TAG ON TAG.id = tag_id\nWHERE entry_id = ?",(id,))
    all_tags = retrievenop('SELECT id, name FROM TAG')
    folders = retrievenop('SELECT id, name FROM FOLDER')
    return render_template('pages/edit.html',information=information,tags=tags,all_tags=all_tags,folders=folders)


#edits an entry based on entered info
@app.route('/edit-entry/<int:id>',methods=["POST"])
def entry_edited(id):
    name = request.form.get('name')
    entry = request.form.get('entry')
    parent_id = request.form.get('folder')
    insert("UPDATE ENTRY SET (parent_id,name,entry) = (?,?,?) WHERE id = ?",(parent_id,name,entry,id))
    insert("DELETE FROM ENTRYTAG WHERE entry_id = ?",(id,))
    enter_tags(id)
    return render_template('pages/home.html')


#displays all tags
@app.route('/all-tags')
def tags():
    tags = retrievenop('SELECT id, name FROM TAG')
    return render_template('pages/tags.html',tags=tags)


#displays a tag, its info and the subjects under it
@app.route('/tag/<int:id>')
def tag(id):
    infoname = retrieve('SELECT name, info FROM TAG WHERE id = ?',(id,))
    entries = retrieve('SELECT id, name FROM ENTRYTAG\nJOIN ENTRY ON ENTRY.id = entry_id\nWHERE tag_id = ?',(id,))
    return render_template('pages/tag.html',infoname=infoname,entries=entries,id=id)


#displays a form with the parameters for a tag 
@app.route('/create-tag')
def create_tag():
    return render_template('pages/create_tag.html')


#enters the information from a submitted one of the form above into the db
@app.route('/create-tag',methods=["POST"])
def tag_creation():
    name = request.form.get('name')
    info = request.form.get('info')
    insert("INSERT INTO TAG(name,info) VALUES (?,?)",(name,info))
    return render_template('pages/home.html')


#A page that provides a form for editing an existing tag
@app.route('/edit-tag/<int:id>')
def edit_tag(id):
    info = retrieve('SELECT name, info FROM TAG WHERE id = ?',(id,))
    return render_template('pages/edit_tag.html',info=info[0])


#edits a tag based on entered info
@app.route('/edit-tag/<int:id>',methods=["POST"])
def tag_edited(id):
    name = request.form.get('name')
    info = request.form.get('info')
    insert("UPDATE TAG SET (name,info) = (?,?) WHERE id = ?",(name,info,id))
    return render_template('pages/home.html')


if __name__=='__main__':
    app.run(debug=True)