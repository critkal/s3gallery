import os
import flask_login
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from helpers import *
from functions import *

app = Flask(__name__)
app.config.from_object("config")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

users = {'gabriel@email.com': {'password': '123'},
        'email@email.com': {'password': '321'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    #load public gallery
    approved = mongo_list_approved()
    return render_template('home.html', imgs = approved)

@app.route('/upload', methods=['POST'])
@flask_login.login_required
def upload_file():
	# A
    if "user_file" not in request.files:
        return "No user_file key in request.files"+ '<br>\
						                            <form action="/upload" method="get">\
						                                <button type="submit">Try Again</button><br>\
						                            </form>'

	# B
    file    = request.files["user_file"]

	# C.
    if file.filename == "":
        return "Please select a file" + '<br>\
			                            <form action="/upload" method="get">\
			                                <button type="submit">Try Again</button><br>\
			                            </form>'

	# D.
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return str(output)

    else:
        return redirect("/upload")

@app.route('/upload/')
@flask_login.login_required
def upload():
	return render_template('upload.html')

@app.route('/validation', methods=['POST'])
def approve():
	o_id = request.form[_id]
	print (o_id)
	return mongo_validate(o_id)

@app.route('/validation/')
#@flask_login.login_required
def validation():
	not_approved = mongo_list_unvalid()
	#local = []
	#for i in imgsrc:
	#	local.append(i['local'])
	return render_template('validation.html', imgsrc=not_approved)

	

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('home'))

    return 'Bad login'

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)