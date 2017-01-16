# Author: Saif Rizvi
# RESTful URL shortening service 

from flask import Flask, request, redirect, abort, jsonify
from flaskext.mysql import MySQL
import validators


app = Flask(__name__)

mysql = MySQL()

# MOVE THIS TO A DIFFERENT FILE (?)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'si14isdopeyo'
app.config['MYSQL_DATABASE_DB'] = 'urlstorage'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Handles incoming POST requests to shorten new URL
@app.route('/services/shortener', methods = ['POST'])
def api_shorten_requests():
	
	# Request must have a JSON body
	if not request.json:
		abort(400)
	
	# Grab requested url from body
	longURL = request.json['longURL']
	
	# Verify valid url formatting
	if not validators.url(longURL):
		return jsonify(error="Please use valid URL. Remember to include http(s)://",longURL=longURL)

	# Connect to DB and get cursor
	cursor = mysql.connect().cursor()
	
	# Check if url already in db
	cursor.callproc('GetRecordFromLongURL', [longURL])
	data = cursor.fetchone()

	if not data:
		cursor.callproc('AddNewURL', [longURL])
		cursor.callproc('GetRecordFromLongURL', [longURL])
		data = cursor.fetchone()
	
	cursor.close()

	# Return json object with details of new shortened URL
	return jsonify(shortURL=data[0], longURL=data[1])	

# Make a separate path for API GET requests, returns info
# @app.route('/api/v1/<shortURL>', )

# Redirects user to URL corresponding to given shortURL if it exists
@app.route('/<shortURL>', methods = ['GET'])
def api_get_shortURL(shortURL):

	# Ignore weird request Chrome keeps sending
	if "favicon" in shortURL:
		pass

	# Query urlDB for shortURL's corresponding longURL
	cursor = mysql.connect().cursor()

	cursor.callproc('GetRecordFromShortURL', [shortURL])
	data = cursor.fetchone()
	cursor.close()

	if data is None:
		return abort(404) # implement custom error response
	else:
		return redirect(data[1], 302)

# TODO: Check if url is in base 62 and 6 chars max
def validateShortURL(url):
	pass

if __name__ == '__main__':
	app.run()