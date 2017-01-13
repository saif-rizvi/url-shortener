# Author: Saif Rizvi

import hashlib
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def api_root():
	if 'POST' in request.args:
		# grab requested url from body
		# verify valid url formatting
		# pass it through shortenURL()
		# check if url in db.. do <something> if it is??
		# return shortened url
		return 'Dope, thanks bro.\n'
	else:
		return "Welcome. POST a long url to get a shortened url back.\n{'longURL' : '<longURL>'}"

@app.route('/<shortURL>', methods = ['GET'])
def api_shortURL(shortURL):
	# query urlDB for shortURL's corresponding longURL
	# if response is NULL
	# 	return 404 Not Found error
	# else
	# 	increment shortURL's counter by one
	# 	return redirect(<longURL>, 302)

def shortenURL(url):
	# md5 hash url 
	# convert to base 62 representation (or 64 if i decide to use - and _) as string
	# return shortenedURL

if __name__ == '__main__':
	app.run()