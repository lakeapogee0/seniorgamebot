from flask import Flask, request, Response

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/foo', methods=["POST"])
def foo_page():
    req_data = request.get_json()
    message = req_data['message']
    print(message)
    return Response(status=200)
