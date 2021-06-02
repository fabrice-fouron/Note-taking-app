from enum import unique
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)  # The app/server running
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)  # The database


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # The unique of each note stored in the database
    date = db.Column(db.DateTime, default=datetime.datetime.today())  # The time the note was created or modified
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
    return render_template('shownotes.html', table=table)


@app.route("/display")
def display():  # Display the note
    '''Display the note'''
    return render_template('display.html')

@app.route('/edit/<string:name>', methods=["GET", "POST"])
def edit_note(name):
    '''View to edit the note'''
    with open(f"./notes/{name}.txt", "r") as f:
        data = f.read()

    if request.method == "POST":
        with open(f"./notes/{name}.txt", "w") as f:
            note = request.form['edit-text']
            f.write(note)
            return redirect("/")

    with open(f"./notes/{name}.txt", "r") as f:
        return render_template("edit.html", text=data)

    
@app.route('/delete/<string:name>', methods=["POST"])
def delete_note(name):  # Remove the note from the database and from the notes folder
    '''Remove the note from the database and from the folder'''
    note = Notes.query.filter_by(title=name).first()
    db.session.delete(note)
    db.session.commit()
    os.remove(f"./notes/{name}.txt")
    return redirect("/shownotes")


def save_note(title, text):  # Save the notes in the notes folder and in the database
    '''Save the notes into the databse and in the folder'''
    f = open(os.path.join("./notes/", f"{title}.txt"), "w")
    f.write(text)
    note = Notes(title=request.form['title'])
    db.session.add(note)


@app.route('/rename/<string:name>', methods=["GET", "POST"])
def rename_note(name):
    '''Changethe name of the note from the original name to after'''
    if request.method == "POST":
        # Change the file name
        new = request.form['new-name']
        os.rename(f"./notes/{name}.txt", f"./notes/{new}.txt")

        # Change the name in the database
        note = Notes.query.filter_by(title=name).first()
        note.title = new
        note.date = datetime.datetime.today()
        db.session.commit()

        # Redirect to the table page
        return redirect("/shownotes")


    return render_template('rename.html')


if __name__ == "__main__":
    app.run(debug=True)
