from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

from threading import Lock

import secrets
import json
import time
import string
import random

app = Flask(__name__)
app.secret_key = secrets.token_hex()



session_users_data = {}
session_ips = []  # update using db or json
session_users = []
session_users_ips = {}


app = Flask(__name__)
app.config["SECRET_KEY"] = "HackCampProject123!"
socketio = SocketIO(app)

rooms = {}
room_names = []
def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    return code


@app.route('/')
def home_page():  # put application's code here
    current_ip = request.remote_addr
    if request.remote_addr in session_ips:
        print(session)
        return render_template('index.html', session_user=session_users_data[session_users_ips[current_ip]], session_users=session_users, session=session_users_data)
    else:
        return render_template('login.html')


@app.route('/signup', methods=["POST", "GET"])
def signup():
    username = request.form['username']
    print("The username is '" + username + "'")
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    current_ip = request.remote_addr
    if current_ip in session_ips:
        return render_template("index.html", session_user=session_users_data[session_users_ips[current_ip]], session_users=session_users, session=session_users_data)
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

                session_users_data[username] = user_data
                session_users_ips[current_ip] = username

                save_to_json(user_data)
                print(session_users_data)
                return render_template('index.html', session_user=session_users_data[session_users_ips[current_ip]], session_users=session_users, session=session_users_data)

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


# chatroom features
@app.route('/chatroom', methods=["POST", "GET"])
def home():
    current_ip = request.remote_addr
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name, room_list=room_names, room_data=rooms)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name, room_list=room_names, room_data=rooms)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name, room_list=room_names, room_data=rooms)
        
        session["room"] = room
        session["name"] = name
        print(rooms)
        print(room_names)
        return redirect(url_for("room"))

    return render_template("home.html", room_list=room_names, room_data=rooms)


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


if __name__ == "__main__":
    socketio.run(app, debug=True)

