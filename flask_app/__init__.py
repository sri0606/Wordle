import os
from flask import Flask
from flask_failsafe import failsafe
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#--------------------------------------------------
# Create a Failsafe Web Application
#--------------------------------------------------
@failsafe
def create_app(debug=False):
	app = Flask(__name__)

	# This will prevent issues with cached static files
	app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
	app.debug = debug
	# The secret key is used to cryptographically-sign the cookies used for storing the session data.
	app.secret_key = os.environ.get("APP_SECRET_KEY")
	# ----------------------------------------------

	from .utils.database.database import database
	db = database()
	db.createTables(purge=True)

	# This will create a user
	db.createUser(email='owner@email.com' ,password='password', role='owner')
	db.createUser(email='ron@email.com' ,password='password', role='player')
	db.createUser(email='kyle@email.com' ,password='password', role='player')
	db.createUser(email='trump@email.com' ,password='password', role='player')
	db.createUser(email='biden@email.com' ,password='password', role='player')

	# ----------------------------------------------

	with app.app_context():
		from . import routes
		return app
