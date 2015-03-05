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
    nb_genres = Genre.query.count()
    nb_keywords = Keyword.query.count()
    nb_languages = Language.query.count()
    nb_shelves = Shelf.query.count()
    return render_sidebar_template('index.html',
                            title='Accueil',
                            nb_authors=nb_authors,
                            nb_books=nb_books,
                            nb_genres=nb_genres,
                            nb_keywords=nb_keywords,
                            nb_languages=nb_languages,
                            nb_shelves=nb_shelves)

@app.route('/auteurs')
def authors():
    authors = Author.query.order_by(Author.aut_last_name).all()
    nb_authors = len(authors)
    return render_sidebar_template('authors.html', title='Auteurs',
                            nb_authors=nb_authors, authors=authors)

@app.route('/auteurs/<author_key>')
def author(author_key):
    author = Author.query.filter(Author.aut_key == author_key).first_or_404()
    books = Title.query.join(Book).join(Author, Title.author_title).filter(Title.tit_id == Book.boo_main_title, Author.aut_id == author.aut_id).order_by(Title.tit_title).all()
    languages = Language.query.join(Title).join(Author, Title.author_title).filter(Author.aut_id == author.aut_id).all()
    genres = Genre.query.join(Title, Genre.title_genre).join(Author, Title.author_title).filter(Author.aut_id == author.aut_id).all()
    if author is not None:
        title = author.aut_last_name.capitalize()
        return render_sidebar_template('author.html',
                                title=title,
                                author=author,
                                books=books,
                                languages=languages,
                                genres=genres)
    else:
        return render_template('404.html'), 404

@app.route('/livres')
def books():
    books = Title.query.join(Book).filter(Title.tit_id == Book.boo_main_title)\
            .order_by(Title.tit_title).all()
    return render_sidebar_template('books.html', title='Livres', books=books)

@app.route('/livres/<book_key>')
def book(book_key):
    book = Title.query.join(Book).filter(Title.tit_id == Book.boo_main_title,
            Title.tit_key == book_key).order_by(Title.tit_title).first_or_404()
    #authors = Author.query.join(Title, Author.title_author).filter(Author. == author_key).all()
    title = book.tit_title.capitalize()
    return render_sidebar_template('book.html',
                                book=book)

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
