id = "abcdefg"
print(id)
from flask import Flask, request
import requests
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)

#if __name__ == '__main__':
    #app.debug = True
    #app.run()


# GET requests will be blocked
@app.route('/foo', methods=['POST'])
def foo():
    load_dotenv()
    botId = os.getenv('BOT_ID')
    print("this is id" + botId)
    request_data = request.get_json()
    if request_data["name"] == "test":
        pass
    elif "❌💀" in request_data["text"]:
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
