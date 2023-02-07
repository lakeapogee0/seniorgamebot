id = "abcdefg"
print(id)
from flask import Flask, request

app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run()


# GET requests will be blocked
@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = request_data['name']
    framework = request_data['text']


    boolean_test = request_data['user_id']

    return '''
           The language value is: {}
           The framework value is: {}
           The boolean value is: {}'''.format(language, framework, boolean_test)