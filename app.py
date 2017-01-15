# Author: Saif Rizvi
# RESTful URL shortening service 

from flask import Flask, request, redirect, abort
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

# Handles incoming POST requests
@app.route('/', methods = ['POST'])
def api_root():
	
	# There's probably a better way to do this
	if not request.json:
		abort(400)
	
	# grab requested url from body
	longURL = request.json['longURL']
	
	# verify valid url formatting. Note: Must start with http(s)://
	if not validators.url(longURL):
		return request.jsonify('{error : "Please use full URL"}')

	# Connect to DB and get cursor
	cursor = mysql.connect().cursor()
	
	# Check if url already in db
	cursor.execute('SELECT * FROM urls WHERE longURL ="' + longURL + '"')
	data = cursor.fetchone()

	# if data is None:
		# cursor.callproc('AddNewURL', longURL)

	# return json object with details of new shortened URL

# Redirects user to URL corresponding to given shortURL if it exists
@app.route('/<shortURL>', methods = ['GET'])
def api_shortURL(shortURL):

	# Ignore weird request Chrome keeps sending
	if "favicon" in shortURL:
		pass
	
	# query urlDB for shortURL's corresponding longURL
	cursor = mysql.connect().cursor()
	cursor.callproc('GetLongURL', shortURL)
	data = cursor.fetchone()
	cursor.close()

	if data is None:
		return abort(404) # implement custom error response
	else:
		return redirect(data[0], 302) # is this unsafe?

# TODO: Check if url is in base 62 and 6 chars max
def validateShortURL(url):
	pass

# base10 to base62 converter. Implement MySQL procedure to use instead of this.
def base10ToBase62(urlID):
	if urlID is 0:
		return "0"

	base62 = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:'a',
				11:'b',12:'c',13:'d',14:'e',15:'f',16:'g',
				17:'h',18:'i',19:'j',20:'k',21:'l',22:'m',
				23:'n',24:'o',25:'p',26:'q',27:'r',28:'s',
				29:'t',30:'u',31:'v',32:'w',33:'x',34:'y',
				35:'z',36:'A',37:'B',38:'C',39:'D',40:'E',
				41:'F',42:'G',43:'H',44:'I',45:'J',46:'K',
				47:'L',48:'M',49:'N',50:'O',51:'P',52:'Q',
				53:'R',54:'S',55:'T',56:'U',57:'V',58:'W',
				59:'Z',60:'X', 61:'Y',62:'Z'}
	
	# Repeated division method
	output = []
	dividend = urlID
	remainder = 0
	while dividend > 0:
		dividend, remainder = divmod(dividend,62)
		output.append(base62[remainder]) 
	return "".join[]

if __name__ == '__main__':
	app.run()