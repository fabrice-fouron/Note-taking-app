from enum import unique
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)  # The app/server running
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)  # The database itself


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # The unique of each note stored in the database
    date = db.Column(db.DateTime, default=datetime.datetime.today())  # The time the note was created or modified
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    title = db.Column(db.String(50), nullable=False, unique=True)  # the title of the note


@app.route("/")  # Decorator to show the route of the page to render in the browser
def index():
    return render_template('index.html')


@app.route("/enternote", methods=['GET', 'POST'])
def enternote():
    '''View to enter the note and save it'''
    if request.method == "GET":  # Simply open the page
        return render_template('enternote.html')
    else:  # If the action is to post, do the following
        note = Notes(title=request.form['title'])
        db.session.add(note)
        db.session.commit()
        save_note(request.form['title'], request.form['enternote'])  # Saves the note to the file
        return redirect("/")  # Redirect to the main page


@app.route("/shownotes", methods=["GET", "POST"])
def shownotes():
    '''View to display the table of notes'''
    table = Notes.query.order_by(Notes.date).all()
    return render_template('shownotes.html', table=table, noUnderscore=no_underscore)


@app.route('/display/<string:name>', methods=["GET", "POST"])
def display(name):  # Display the note
    '''Display the note'''
    with open(f"./notes/{underscore(name)}.txt", "r") as f:
        data = f.read()

    if request.method == "POST":
        return redirect("/")
    return render_template('display.html', text=data)

@app.route('/edit/<string:name>', methods=["GET", "POST"])
def edit_note(name):
    '''View to edit the note'''
    with open(f"./notes/{underscore(name)}.txt", "r") as f:
        data = f.read()

    if request.method == "POST":
        with open(f"./notes/{underscore(name)}.txt", "w") as f:
            note = request.form['edit-text']
            f.write(note)
            obj = Notes.query.filter_by(title=no_underscore(name)).first()
            obj.date = datetime.datetime.today()
            obj.time = datetime.datetime.now()
            db.session.commit()
            return redirect("/shownotes")

    with open(f"./notes/{underscore(name)}.txt", "r") as f:
        return render_template("edit.html", text=data)

    
@app.route('/delete/<string:name>', methods=["GET", "POST"])
def delete_note(name):  # Remove the note from the database and from the notes folder
    '''Remove the note from the database and from the folder'''
    note = Notes.query.filter_by(title=no_underscore(name)).first()
    db.session.delete(note)
    db.session.commit()
    os.remove(f"./notes/{underscore(name)}.txt")
    return redirect("/shownotes")


def save_note(title, text):  # Save the notes in the notes folder and in the database
    '''Save the notes into the databse and in the folder'''
    f = open(os.path.join("./notes/", f"{underscore(title)}.txt"), "w")
    f.write(text)
    note = Notes(title=request.form['title'])
    db.session.add(note)


@app.route('/rename/<string:name>', methods=["GET", "POST"])
def rename_note(name):
    '''Change the name of the note from the original name to after'''
    if request.method == "POST":
        # Change the file name
        new = request.form['new-name']
        os.rename(f"./notes/{underscore(name)}.txt", f"./notes/{underscore(new)}.txt")

        # Change the name in the database
        note = Notes.query.filter_by(title=no_underscore(name)).first()
        note.title = new
        note.date = datetime.datetime.today()
        note.time = datetime.datetime.now()
        db.session.commit()

        # Redirect to the table page
        return redirect("/shownotes")


    return render_template('rename.html')

def underscore(name):  # Replace the space in the title to a underscore
  if " " in name:
    return name.replace(" ", "_")
  return name

def no_underscore(name):  # Replace the underscore in the filename to a space
  if "_" in name:
    return name.replace("_", " ")
  return name

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
