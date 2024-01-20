from flask import Flask

from flask import request, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    print("The username is '" + username + "'")
    return redirect('/')


if __name__ == '__main__':
    app.run()
