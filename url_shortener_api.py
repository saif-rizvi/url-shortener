# RESTful API to interface with url-shortener service
# Author: Saif Rizvi 

import requests

# Sends a POST request to API to shorten new URL
# Returns response object
def shortenURL(longURL):
	return requests.post(_url("services/shortener"), json={
		"longURL":longURL
		})

# Sends a GET request to API
# Returns response object
def getRedirectInfo(shortURL):
	return requests.get(_url("api/json/"+shortURL), json={
		"shortURL":shortURL
		})

# format URL for requests
def _url(path):
	return "http://127.0.0.1:5000/" + path
