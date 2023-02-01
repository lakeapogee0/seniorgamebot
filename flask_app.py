
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for
from flash_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config{"DEBUG"} = True

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        messages.append(request.form)

class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))


messages = []

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="lake0",
    password="wowadatabase:)",
    hostname="lake0.mysql.pythonanywhere-services.com",
    databasename="lake0$messages",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

