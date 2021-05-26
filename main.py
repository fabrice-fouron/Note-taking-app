from enum import unique
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # The unique of each note stored in the database
    date = db.Column(db.DateTime, default=datetime.datetime.today())  # The time the note was created or modified
    title = db.Column(db.String(50), nullable=False, unique=True)  # the title of the note


@app.route("/")  # Decorator to show the route of the page to render in the browser
def index():
    return render_template('index.html')


@app.route("/enternote", methods=['GET', 'POST'])
def enternote():
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
    table = Notes.query.order_by(Notes.date).all()
    return render_template('shownotes.html', table=table)


@app.route("/display")
def display():  # Display the note
    return render_template('display.html')

@app.route('/edit/<string:name>', methods=["POST", "GET"])
def edit_note(name):
    newFile = open(os.path.join("./notes/", f"{name}A.txt"), "w")# Going to create a new file to replace the previous one
    with open(f"./notes/{name}.txt", "r") as f:
        newFile.write(f.read())
    os.remove(f"./notes/{name}.txt")  # Make sure to keep both names different to avoid conflict and then rename later to the original name
    os.rename(f"./notes/{name}A.txt", f"./notes/{name}.txt")
    newFile = open(f"./notes/{name}.txt", "r")
    return render_template("edit.html", text=newFile.read())


def save_note(title, text):  # Save the notes in the notes folder and in the database
    f = open(os.path.join("./notes/", f"{title}.txt"), "w")
    f.write(text)
    note = Notes(title=request.form['title'])
    db.session.add(note)
    
@app.route('/delete/<string:name>', methods=["POST"])
def delete_note(name):  # Remove the note from the database and from the notes folder
    note = Notes.query.filter_by(title=name).first()
    db.session.delete(note)
    db.session.commit()
    os.remove(f"./notes/{name}.txt")
    return redirect("/shownotes")


if __name__ == "__main__":
    app.run(debug=True)
