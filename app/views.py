from collections import OrderedDict
from flask import render_template, url_for, redirect, request
from flask.ext.sqlalchemy import get_debug_queries
from app import app, db
from .models import *


def render_sidebar_template(template_name, **kwargs):
    sidebar_genres = db.session.query(Genre.gnr_label, Genre.gnr_key, db.func.count(Genre.gnr_label).label('count_genre')).join(Title, Genre.title_genre).join(Book, Title.tit_book_main).group_by(Genre.gnr_label, Genre.gnr_key).order_by(Genre.gnr_key).all()
    return render_template(template_name, sidebar_genres=sidebar_genres, **kwargs)


@app.route('/')
def index():
    nb_authors = Author.query.count()
    authors = db.session.query(db.func.substr(db.func.upper(Author.aut_last_name), 1, 1).label('first_letter')).group_by('first_letter').all()
    aut_first_letters = OrderedDict()
    for letter in('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        aut_first_letters[letter] = False
    for letter in authors:
        aut_first_letters[letter[0]] = True

    nb_books = Book.query.count()
    books = db.session.query(db.func.substr(db.func.upper(Title.tit_title), 1, 1).label('first_letter')).join(Book).group_by('first_letter').all()
    boo_first_letters = OrderedDict()
    for letter in('0ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        if letter == '0':
            boo_first_letters['[0-9]'] = False
        else:
            boo_first_letters[letter] = False
    for letter in books:
        if letter[0] in('0123456789'):
            boo_first_letters['[0-9]'] = True
        else:
            boo_first_letters[letter[0]] = True

    nb_genres = Genre.query.count()
    nb_keywords = Keyword.query.count()
    nb_languages = Language.query.count()
    nb_shelves = Shelf.query.count()
    return render_sidebar_template('index.html',
                            title='Accueil',
                            nb_authors=nb_authors,
                            aut_first_letters=aut_first_letters,
                            nb_books=nb_books,
                            boo_first_letters=boo_first_letters,
                            nb_genres=nb_genres,
                            nb_keywords=nb_keywords,
                            nb_languages=nb_languages,
                            nb_shelves=nb_shelves)

@app.route('/auteurs')
def authors():
    authors = Author.query.order_by(Author.aut_last_name).all()
    return render_sidebar_template('authors.html', title='Auteurs', authors=authors)

@app.route('/auteurs/<author_key>')
def author(author_key):
    author = Author.query.filter(Author.aut_key == author_key).first_or_404()
    books = Title.query.join(Book).join(Author, Title.author_title).filter(Title.tit_id == Book.boo_main_title, Author.aut_id == author.aut_id).order_by(Title.tit_title).all()
    languages = Language.query.join(Title).join(Author, Title.author_title).filter(Author.aut_id == author.aut_id).all()
    genres = Genre.query.join(Title, Genre.title_genre).join(Author, Title.author_title).filter(Author.aut_id == author.aut_id).all()
    if author is not None:
        title = 'Auteur: ' + author.aut_last_name.capitalize()
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
            .order_by(Title.tit_key).all()
    return render_sidebar_template('books.html', title='Livres', books=books)

@app.route('/livres/<book_key>')
def book(book_key):
    main_title = Title.query.join(Book).filter(Title.tit_id == Book.boo_main_title,
            Title.tit_key == book_key).order_by(Title.tit_key).first_or_404()
    title = 'Livre: ' + main_title.tit_title
    book = Book.query.join(Title, Book.title_book_main).filter(Title.tit_id == main_title.tit_id).first()
    authors = Author.query.join(Title, Author.title_author).filter(Title.tit_id == main_title.tit_id).order_by(Author.aut_last_name).all()
    languages = Language.query.join(Title).filter(Title.tit_id == main_title.tit_id).all()
    shelf = Shelf.query.join(Copy).join(Book).join(Title).filter(Title.tit_id == main_title.tit_id).first()
    genres = Genre.query.join(Title, Genre.title_genre).filter(Title.tit_id == main_title.tit_id).all()
    subtitles = Title.query.join(Book, Title.book_title_sec).filter(Book.boo_id == book.boo_id, Title.tit_id != main_title.tit_id).order_by(Title.tit_key).all()
    return render_sidebar_template('book.html', title=title,
                                    main_title=main_title,
                                    authors=authors,
                                    languages=languages,
                                    shelf=shelf,
                                    genres=genres,
                                    subtitles=subtitles)

@app.route('/genres')
def genres():
    # Attention: requires data from 'render_sidebar_template'.
    return render_sidebar_template('genres.html', title='Genres')

@app.route('/genres/<genre_key>')
def genre(genre_key):
    genre = Genre.query.filter(Genre.gnr_key == genre_key).first_or_404()
    page_title = 'Genre: ' + genre.gnr_label.lower()
    books = Title.query.join(Book).join(Genre, Title.genre_title).filter(Title.tit_id == Book.boo_main_title, Genre.gnr_id == genre.gnr_id).order_by(Title.tit_key).all()
    return render_sidebar_template('genre.html',
                                title=page_title,
                                genre=genre,
                                books=books)

@app.route('/langues')
def languages():
    languages = Language.query.order_by(Language.lng_label).all()
    languages = db.session.query(Language.lng_label, Language.lng_key, db.func.count(Language.lng_label).label('count_language')).join(Title, Language.lng_title).join(Book, Title.tit_book_main).group_by(Language.lng_label, Language.lng_key).order_by(Language.lng_key).all()
    return render_sidebar_template('languages.html', title='Langues', languages=languages)

@app.route('/langues/<language_key>')
def language(language_key):
    language = Language.query.filter(Language.lng_key == language_key).first_or_404()
    page_title = 'Langue: ' + language.lng_label.lower()
    books = Title.query.join(Book).join(Language).filter(Title.tit_id == Book.boo_main_title, Language.lng_id == language.lng_id).order_by(Title.tit_key).all()
    return render_sidebar_template('language.html',
                                title=page_title,
                                language=language,
                                books=books)

@app.route('/rayons')
def shelves():
    shelves = Shelf.query.order_by(Shelf.shl_key).all()
    return render_sidebar_template('shelves.html', title='Rayons', shelves=shelves)

@app.route('/rayons/<shelf_key>')
def shelf(shelf_key):
    shelf = Shelf.query.filter(Shelf.shl_key == shelf_key).first_or_404()
    page_title = 'Rayon: ' + shelf.shl_label.upper()
    books = Title.query.join(Book).join(Copy).join(Shelf).filter(Shelf.shl_key == shelf.shl_key).order_by(Title.tit_key).all()
    return render_sidebar_template('shelf.html', title=page_title, shelf=shelf, books=books)

@app.route('/a-propos')
def about():
    return render_template('about.html', title='A propos')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
