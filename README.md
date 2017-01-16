# url-shortener


### a RESTful url shortening service using python/flask/mysql

* POST /services/shortener : Adds given URL to database and returns shortened url
* GET /\<shortURL> : (In browser) Redirects user to original url
* GET /api/json/\<shortURL> : Returns JSON object of shortened url and original long url 

Dependencies:
```shell 
pip install flask
pip install flask-mysql
pip install requests
pip install validators
```
