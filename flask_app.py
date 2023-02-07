import os
import json


from urllib.parse import urlencode
from urllib.request import Request, urlopen
id = "abcdefg"
print(id)
from flask import Flask, request

app = Flask(__name__)


@app.route('/foo', methods=["POST"])
def foo_page():
    data = request.get_json()
    msg = data
    print(msg)
    send_message(msg)
    return "ok", 200

def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'

  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = Request(url, urlencode(data).encode())
  #json = urlopen(request).read().decode()