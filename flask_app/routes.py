from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context,jsonify
from .utils.database.database  import database
from .utils.wordle.wordle  import scrape_word_of_day,spell_check
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools

db = database()
word_of_day = scrape_word_of_day()

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
	return db.reversibleEncrypt('decrypt',session['email']) if 'email' in session else 'Unknown'

def getUserName():
     return str(db.reversibleEncrypt('decrypt',session['email'])).split('@')[0] if 'email' in session else 'Unknown'

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
	if request.method == 'POST':
            form_fields = request.form.to_dict()

            email = form_fields.get('email')
            password = form_fields.get('password')

            # Add your authentication logic here
            authentication_result = db.authenticate(email, password)

            if authentication_result['success'] == 1:
                # Authentication successful, update the user's session
                session['email'] = db.reversibleEncrypt('encrypt', email) 

            # Return the status of the authentication as a JSON object
            return json.dumps(authentication_result)


@app.route('/processsignup', methods = ["POST","GET"])
def processsignup():
        if request.method == 'POST':
            form_fields = request.form.to_dict()

            email = form_fields.get('email')
            password = form_fields.get('password')

            creation_result = db.createUser(email, password)

            if creation_result['success'] == 1:
                # Authentication successful, update the user's session
                session['email'] = db.reversibleEncrypt('encrypt', email) 

            # Return the status of the authentication as a JSON object
            return json.dumps(creation_result)

#######################################################################################
# General
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html', user=getUserName())

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


@app.route('/processfeedback', methods = ['GET','POST'])
def processfeedback():
	feedback = request.form
	db.addFeedbackData(feedback)
	feedback_data = db.getFeedbackData()
	print(feedback_data)
	return render_template('processfeedback.html', feedback_data = feedback_data)

#######################################################################################
# Game RELATED
#######################################################################################
@app.route('/get_word_of_day')
def get_word_of_day():
    return jsonify({'hidden_word': word_of_day})

@app.route('/spell_check', methods=['POST','GET'])
def spell_check_route():
    if request.method == 'POST':
        data = request.get_json()
        word_to_check = data.get('word')
        spell_check_result = spell_check(word_to_check)

        return json.dumps(spell_check_result)

@app.route('/leaderboard')
def leaderboard():
    # Retrieve user information from the database
    leaderboard_dict = db.get_top_five()
    return jsonify({'leaderboard' : leaderboard_dict})

@app.route('/update_time_taken', methods=['POST'])
def time_taken():
    data = request.get_json()
    time_elapsed = data['time_elapsed']
    # update time taken to finish the game
    current_user_email = getUser()
    db.update_time_taken(current_user_email, time_elapsed)

    return jsonify({"success":1})