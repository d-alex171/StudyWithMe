<<<<<<< Updated upstream
from flask import Flask
=======
from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
from threading import Lock
import secrets
import json
import time
import string
import random
>>>>>>> Stashed changes

app = Flask(__name__)
app.secret_key = secrets.token_hex()

session = {}
session_ips = []  # update using db or json
session_users = []
session_users_ips = {}


@app.route('/')
def home_page():  # put application's code here
    current_ip = request.remote_addr
    if request.remote_addr in session_ips:
        print(session)
        return render_template('index.html', session_user=session[session_users_ips[current_ip]], session_users=session_users)
    else:
        return render_template('login.html')


<<<<<<< Updated upstream
=======
@app.route('/signup', methods=['GET'])
def signup():
    username = request.form['username']
    print("The username is '" + username + "'")
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    current_ip = request.remote_addr
    if current_ip in session_ips:
        return render_template("index.html", session_user=session[session_users_ips[current_ip]], session_users=session_users)
    else:
        if request.method == 'POST':
            username = request.form['username']
            location = request.form['location']
            course = request.form['course']
            last_action_time = time.gmtime()
            chat_code = generate_chat_code()

            if username in session_users:
                return render_template("login.html")
            else:
                user_data = [username, location, course, last_action_time, current_ip, chat_code]
                session_ips.append(current_ip)
                session_users.append(username)

                session[username] = user_data
                session_users_ips[current_ip] = username

                save_to_json(user_data)
                print(session)
                return render_template('index.html', session_user=session[username], session_users=session_users)

    return render_template('login.html')


def generate_chat_code():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))
    return result_str


def save_to_json(data):
    user = {
        data[0]: {
            "username":    data[0],
            "location":    data[1],
            "course":      data[2],
            "last_action": data[3],
            "ip_address":  data[4],
            "chat_code":   data[5]
        }
    }
    user_json = json.dumps(user)

    with open("userData.json", "w") as write_file:
        json.dump(user_json, write_file)


>>>>>>> Stashed changes
if __name__ == '__main__':
    app.run()
