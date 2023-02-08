id = "abcdefg"
print(id)
from flask import Flask, request, render_template
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


def getId():
    load_dotenv()
    botId = os.getenv('BOT_ID')
    return botId

stat = "no one is out of the game"
# GET requests will be blocked
@app.route('/foo', methods=['POST'])
def foo():
    botId = getId()
    request_data = request.get_json()
    if request_data["name"] == "test":
        pass
    elif "❌💀" in request_data["text"]:
        global stat
        stat = request_data["name"] + " is out of the game!💀"
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

@app.route('/', methods=['GET'])
def index():
       return render_template("index.html", stat=stat)



