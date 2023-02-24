id = "abcdefg"
print(id)
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, select, MetaData, Table, UniqueConstraint, Index #this isn't working -- it should allow unique checking between 2 columns in SQL
from sqlalchemy.exc import IntegrityError #chatGPT showed me error handling
import mysql.connector
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

#with db.session() as session:
 #   results = session.execute("SELECT * FROM deathTable")
  #  for row in results:
   #     print(row)


#https://stackoverflow.com/questions/30785892/simple-select-statement-on-existing-table-with-sqlalchemy


#from tutorial - modified for my code of course
#asked chatGPT how to set this up as tutorials had different answers w/o explanation
class Assassin(db.Model):

    __tablename__ = "DeathTable"
    #__table_args__ = (
        #db.UniqueConstraint('murdered', 'witnessed'),)
        #UniqueConstraint('murdered', 'witnessed', name='unique_death'),
        #)#unique_death is just the name of the constraint which will be made in SQL (it just needs to call it something)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    murdered = db.Column(db.Boolean)
    witnessed = db.Column(db.Boolean)
    timedout = db.Column(db.Boolean)

    def set_murdered(self, value):
        if value:
            self.witnessed = False
            self.timedout = False
        self.murdered = value

    def set_witnessed(self, value):
        if value:
            self.murdered = False
            self.timedout = False
        self.witnessed = value

    def set_timedout(self, value):
        if value:
            self.murdered = False
            self.witnessed = False
        self.timedout = value

class GameState(db.Model):

    __tablename__ = "GameState"
    id = db.Column(db.Integer, primary_key=True)
    gameState = db.Column(db.Integer)




#Index('unique_death', Assassin.murdered, Assassin.witnessed, unique=True)
#these are the table columns at the moment
def __init__(self, name, murdered, witnessed, timedout, gameState):
    self.name = name
    self.murdered = murdered
    self.witnessed = witnessed
    self.timedout = timedout
    self.gameState = gameState
#creates MySQL table
db.create_all()


#this is my function that allows me to easily grab the bot ID from .env. Seems to work better than a global var, but atm I have to either:
#use getId() wherever I need the ID (so run the function every time), or say botId = getId inside every function. Maybe a global var is the right move since the botId doesn't change.
def getId():
    load_dotenv()
    botId = os.getenv('BOT_ID')
    return botId

#request_data is a global var which gets populated by @app.route /foo. When I send a msg in the chat, it sends an HTML POST in JSON format to this app (request.get_json()). That populates into the global var.
#This global var can be accessed by other sublinks like /
request_data = ""
gameState = None
callbackUrl = "https://api.groupme.com/v3/bots/post"




#game = GameState(gameState=0)
#try:
#    db.session.add(game)
 #   db.session.commit()
#except IntegrityError as e:
 #   db.session.rollback()
    # Handle the unique error
    # for example, you can show an error message to the user:
  #  print('gameState - ERROR: Either was same, or NULL')
   # print(e)


# GET requests will be blocked
@app.route('/foo', methods=['POST'])
def foo():
    botId = getId()
    global request_data
    global gameState
    global callbackUrl
    global name
    global murdered
    global witnessed
    request_data = request.get_json()
    if request_data["name"] == "Jib":
        if request_data["text"] == "///start":
            game = GameState(gameState=1)
            #print("testing the SQL" + request_data["name"] + " is out of the game!💀")
            try:
                db.session.add(game)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                # Handle the unique error
                # for example, you can show an error message to the user:
                print('gameState - ERROR: Either was same, or NULL')
                print(e)
            r = requests.post(callbackUrl, json ={
              "bot_id"  : botId,
              "text"    : "ok say ✅ to join"
              })
        elif request_data["text"] == "///everyonein":
            game = GameState(gameState=2)
            #print("testing the SQL" + request_data["name"] + " is out of the game!💀")
            try:
                db.session.add(game)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                # Handle the unique error
                # for example, you can show an error message to the user:
                print('gameState - ERROR: Either was same, or NULL')
                print(e)
            r = requests.post(callbackUrl, json ={
              "bot_id"  : botId,
              "text"    : "ok, game starting!🤫"
              })
        elif request_data["text"] == "///end":
            game = GameState(gameState=0)
            #print("testing the SQL" + request_data["name"] + " is out of the game!💀")
            try:
                db.session.add(game)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                # Handle the unique error
                # for example, you can show an error message to the user:
                print('gameState - ERROR: Either was same, or NULL')
                print(e)
            r = requests.post(callbackUrl, json ={
              "bot_id"  : botId,
              "text"    : "game ended"
              })
        else:
            pass
    #if the name of the person who sent the message is test, don't respond (that's the bot's name). I will later change this to user_id so it's unique and can't mix up multiple people with the same name.
    #results = db.engine.execute('SELECT gameState FROM deathTable')

    #chatGPT gave me this line
    global gameState_value
    gameState_value = db.session.query(GameState.gameState).order_by(GameState.id.desc()).limit(1).scalar()
    print(gameState_value)
    if request_data["name"] == "test":
            pass
    elif gameState_value == 1 :
        if "✅" in request_data["text"]:
            #I asked chatGPT for clarification on how to set this up because I was getting confused by other sources.
            joinName = Assassin(name=request_data["name"], murdered=False, witnessed=False, timedout=False)
            try:
                db.session.add(joinName)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                # Handle the unique error
                # for example, you can show an error message to the user:
                print('murdered - ERROR: Either name was same, or NULL')
                print(e)
            #r sends a POST back to GroupMe so bot can talk in chat.
            r = requests.post(callbackUrl, json ={
              "bot_id"  : botId,
              "text"    : request_data["name"] + " joined the game"
            })
    elif gameState_value == 2:
        #else if ❌💀 in chat, send to the database that someone is out, and respond with a RIP message
        if "❌💀" in request_data["text"]:
            #I asked chatGPT for clarification on how to set this up because I was getting confused by other sources.
            assassin = Assassin.query.filter_by(name=request_data["name"]).first()
            # Update the timedout attribute
            assassin.set_murdered(True)
            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                # Handle the unique error
                # for example, you can show an error message to the user:
                print('murdered - ERROR: Either name was same, or NULL')
                print(e)
            #r sends a POST back to GroupMe so bot can talk in chat.
            r = requests.post(callbackUrl, json ={
              "bot_id"  : botId,
              "text"    : request_data["name"] + " was assassinated\nRIP 💀"
            })
        elif "❌👀" in request_data["text"]:
            #ChatGPT made this code to change the value rather than add a new one!
            # Retrieve the assassin instance from the database using the name
            assassin = Assassin.query.filter_by(name=request_data["name"]).first()
            # Update the witnessed attribute
            assassin.set_witnessed(True)
            #print("testing the SQL" + request_data["name"] + " is out of the game!💀")
            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                # Handle the unique error
                # for example, you can show an error message to the user:
                print('witnessed - ERROR: Either name was same, or NULL')
                print(e)
            #r sends a POST back to GroupMe so bot can talk in chat.
            r = requests.post(callbackUrl, json ={
              "bot_id"  : botId,
              "text"    : request_data["name"] + " was witnessed\nRIP 👀"
            })
        elif "❌⌛" in request_data["text"] or "❌⏳" in request_data["text"]:
            #I asked chatGPT for clarification on how to set this up because I was getting confused by other sources.
            assassin = Assassin.query.filter_by(name=request_data["name"]).first()
            # Update the timedout attribute
            assassin.set_timedout(True)
            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                # Handle the unique error
                # for example, you can show an error message to the user:
                print('witnessed - ERROR: Either name was same, or NULL')
                print(e)
            #r sends a POST back to GroupMe so bot can talk in chat.
            r = requests.post(callbackUrl, json ={
              "bot_id"  : botId,
              "text"    : request_data["name"] + " timed out\nRIP ⏳"
            })
    elif gameState_value == 0:
        r = requests.post("https://api.groupme.com/v3/bots/post", json ={
          "bot_id"  : botId,
          "text"    : "the game is not currently active"
        })

        print(r.text)
    return Response(status=200)

#attaches a template which connects index.html to sublink / and sends a var over which can be used for logic in HTML.
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", data=Assassin.query.all())




