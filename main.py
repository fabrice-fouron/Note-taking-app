from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    note = db.Column(db.String(2000), nullable=False)
    favorite = db.Column(db.Boolean, default=True, nullable=False) 

@app.route("/")  # Decorator to show the route of the page to render in the browser
def index():
    return render_template('index.html')

@app.route("/enternote", methods=['GET', 'POST'])
def enternote():
    if request.method == "GET":  # Simply open the page
        return render_template('enternote.html')
    else:  # If the action is to post, do the following
        note = Notes(note=request.form['enternote'])
        db.session.add(note)
        db.session.commit()
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
