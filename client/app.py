from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)
@app.route('/',methods=['GET'])
def default():
  print('hello')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000,debug=True)