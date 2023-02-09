id = "abcdefg"
print(id)
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)


#taken from tutorial -- connects to database
#sets a var to the string needed to connect to database
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="lake0",
    password="wowadatabase:)",
    hostname="lake0.mysql.pythonanywhere-services.com",
    databasename="lake0$messages",
)
#saves in Flask config
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
#sets connection to server timeout - time to close unused connections
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
#disables a feature we aren't going to use
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#creates an object for the database using above config
db = SQLAlchemy(app)

#from tutorial - modified for my code of course
#asked chatGPT how to set this up as tutorials had different answers w/o explanation
class Stat(db.Model):

    __tablename__ = "StatData"
    id = db.Column(db.Integer, primary_key=True)
    statRip = db.Column(db.String(4096))

def __init__(self, statRip):
    self.statRip = statRip

db.create_all()


def getId():
    load_dotenv()
    botId = os.getenv('BOT_ID')
    return botId


request_data = ""
# GET requests will be blocked
@app.route('/foo', methods=['POST'])
def foo():
    botId = getId()
    global request_data
    request_data = request.get_json()
    if request_data["name"] == "test":
        pass
    elif "❌💀" in request_data["text"]:
        #I asked chatGPT for clarification on how to set this up because I was getting confused by other sources.
        global statRip
        stat = Stat(statRip=request_data["name"] + " is out of the game!")
        print("testing the SQL" + request_data["name"] + " is out of the game!💀")
        db.session.add(stat)
        db.session.commit()
        r = requests.post("https://api.groupme.com/v3/bots/post", json ={
          "bot_id"  : botId,
          "text"    : request_data["name"] + " was assassinated\nRIP 💀"
        })
    else:
        r = requests.post("https://api.groupme.com/v3/bots/post", json ={
          "bot_id"  : botId,
          "text"    : request_data["text"]
        })

        print(r.text)
    return Response(status=200)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", data=Stat.query.all())




