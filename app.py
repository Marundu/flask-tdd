import sqlite3
from flask import (
    Flask,
    request,
    session,
    g,
    redirect,
    url_for,
    abort,
    render_template,
    flash,
    jsonify,
    )


# configuration 
DATABASE='flaskr.db'
DEBUG=True
SECRET_KEY='iamamasterflasker'
USERNAME='admin'
PASSWORD='admin'


app=Flask(__name__)
app.config.from_object(__name__)


#@app.route('/')
#def hello():
#    return 'Hello, Master Flasker!'


if __name__=='__main__':
    app.run()
