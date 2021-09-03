from flask import Flask, render_template, url_for, request, redirect
from flask.globals import request
from werkzeug.utils import redirect
from datetime import datetime
import requests
import json
import unicodedata
app = Flask(__name__)


@app.route("/home", methods=["GET","POST"])
def index():
    if request.method == 'POST':
        id = request.form['id']
        print(id)
        user = requests.get('http://127.0.0.1:5000/users/'+str(id))
        user = unicodedata.normalize('NFKD', user.text).encode('ascii','ignore')
        data = json.loads(user)

        return render_template('index.html',users = data)

    info = requests.get('http://127.0.0.1:5000/users')
    info = unicodedata.normalize('NFKD', info.text).encode('ascii','ignore')
    data = json.loads(info)

    return render_template('index.html',users = data)



@app.route("/user/create", methods=["GET", "POST"])
def create_a_user():
    if request.method == "POST":
        data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "gender" : request.form['gender'],
        "age" : int(request.form['age']),
        "password" : request.form['password']
        }

        info = requests.post('http://127.0.0.1:5000/users', json=data)

        if info.status_code == 201:
            redirect('/home')
        else:
            error_message = {'error':'Could not create user'}
            return render_template("create.html", message=error_message)
    return render_template('create.html')


@app.route("/user/delete/<int:id>")
def delete(id):
    info = requests.delete('http://127.0.0.1:5000/users/'+str(id))
    if info.status_code == 200:
        return redirect('/home')
    return render_template('delete_error.html')


@app.route("/user/update/<int:id>", methods=["GET", "POST"])
def update(id):
    user = requests.get('http://127.0.0.1:5000/users/'+str(id))
    user = unicodedata.normalize('NFKD', user.text).encode('ascii','ignore')
    user_data = json.loads(user)
    
    print(user_data)

    if request.method == "POST":
        data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "gender" : request.form['gender'],
        "age" : int(request.form['age']),
        "password" : request.form['password']
        }
        
        info = requests.patch('http://127.0.0.1:5000/users/'+str(id), json=data)
        print(info.status_code)
        if info.status_code == 201:
            return redirect('/home')
        else:
            error_message = {'error':'Could not update user'}
            return render_template("update.html", message=error_message)

    # else:
    return render_template("update.html", users=user_data)


if __name__ == "__main__":
    app.run(debug=True, port=8000)