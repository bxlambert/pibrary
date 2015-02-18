from flask import render_template
from flask.ext.sqlalchemy import get_debug_queries
from app import app, db
from .models import *

@app.route('/')
def index():
    authors = Author.query.all()
    test = Author.query.filter(Author.aut_last_name.like('%SIMENON%')).first()
    return render_template('index.html',
                           title='Accueil',
                           authors=authors, test=test)