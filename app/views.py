from flask import render_template, url_for, redirect, request
from flask.ext.sqlalchemy import get_debug_queries
from app import app, db
from .models import *


def render_sidebar_template(template_name, **kwargs):
    sidebar_genres = db.session.query(Genre.gnr_label, db.func.count(Genre.gnr_label).label('count_genre')).join(Title, Genre.title_genre).join(Book, Title.tit_book_main).group_by(Genre.gnr_label).all()
    return render_template(template_name, sidebar_genres=sidebar_genres, **kwargs)


@app.route('/')
def index():
    nb_authors = Author.query.count()
    nb_books = Book.query.count()
    return render_sidebar_template('index.html',
                            title='Accueil',
                            nb_authors=nb_authors,
                            nb_books=nb_books,
                            genres=genres)

@app.route('/auteurs')
def authors():
    authors = Author.query.order_by(Author.aut_last_name).all()
    nb_authors = len(authors)
    return render_sidebar_template('authors.html', title='Auteurs',
                            nb_authors=nb_authors, authors=authors)

@app.route('/auteurs/<author_key>')
def author(author_key):
    author = Author.query.filter(Author.aut_key == author_key).first()
    if author is not None:
        title = author.aut_last_name.capitalize()
        return render_sidebar_template('author.html',
                                title=title,
                                author=author)
    else:
        return render_template('404.html'), 404

@app.route('/livres')
def books():
    books = Title.query.join(Book).filter(Title.tit_id == Book.boo_main_title)\
            .order_by(Title.tit_title).all()
    nb_books = len(books)
    return render_sidebar_template('books.html', title='Livres',
                            nb_books=nb_books, books=books)

@app.route('/genres')
def genres():
    genres = Genre.query.all()
    nb_genres = len(genres)
    return render_sidebar_template('genres.html', title='Genres',
                            nb_genres=nb_genres, genres=genres)

@app.route('/rayons')
def shelves():
    shelves = Shelf.query.all()
    nb_shelves = len(shelves)
    return render_sidebar_template('shelves.html', title='Rayons',
                            nb_shelves=nb_shelves, shelves=shelves)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
