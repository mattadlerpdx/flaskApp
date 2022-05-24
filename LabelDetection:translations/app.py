"""
A simple guestbook flask app.
"""
import flask, os
from flask.views import MethodView
from index import Index
from view import View
from sign import Sign
app = flask.Flask(__name__)       # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods= ["GET"])

app.add_url_rule('/view',
                 view_func=View.as_view('view'),
                 methods=["GET"])
                 

app.add_url_rule('/sign',
                 view_func=Sign.as_view('sign'),
                 methods=[ "GET", "POST"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
