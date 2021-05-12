from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    note = db.Column(db.String(200), nullable=False)
    favorite = db.Column(db.Boolean, nullable=False) 

@app.route("/")  # Decorator to show the route of the page to render in the browser
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
