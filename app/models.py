from app import db

author_title_table = db.Table('lnkAuthorTitle',
    db.Column('lat_author_id', None, db.ForeignKey('tblAuthor.aut_id')),
    db.Column('lat_title_id', None, db.ForeignKey('tblTitle.tit_id'))
)

title_genre_table = db.Table('lnkTitleGenre',
    db.Column('ltg_title_id', None, db.ForeignKey('tblTitle.tit_id')),
    db.Column('ltg_genre_id', None, db.ForeignKey('lstGenre.gnr_id'))
)

title_keyword_table = db.Table('lnkTitleKeyword',
    db.Column('ltk_title_id', None, db.ForeignKey('tblTitle.tit_id')),
    db.Column('ltk_keyword_id', None, db.ForeignKey('lstKeyword.kwd_id'))
)

book_title_table = db.Table('lnkBookTitle',
    db.Column('lbt_book_id', None, db.ForeignKey('tblBook.boo_id')),
    db.Column('lbt_title_id', None, db.ForeignKey('tblTitle.tit_id'))
)

class Author(db.Model):
    __tablename__ = 'tblAuthor'

    aut_id = db.Column(db.String(40), primary_key=True)
    aut_last_name = db.Column(db.String(40), nullable=False)
    aut_first_name = db.Column(db.String(40))
    aut_key = db.Column(db.String(40), nullable=False)
    aut_sex = db.Column(db.String(1), nullable=False)
    aut_birth_date = db.Column(db.DateTime)
    aut_death_date = db.Column(db.DateTime)
    aut_title = db.relationship('Title', secondary=author_title_table, backref='author_title')

    def __repr__(self):
        return "---- Author ----\nid = '%s'\nlast name = '%s'\n" % (self.aut_id, self.aut_last_name)

class Title(db.Model):
    __tablename__ = 'tblTitle'

    tit_id = db.Column(db.String(40), primary_key=True)
    tit_title = db.Column(db.String(100), nullable=False)
    tit_key = db.Column(db.String(40), nullable=False)
    tit_author = db.relationship('Author', secondary=author_title_table, backref='title_author')
    tit_genre = db.relationship('Genre', secondary=title_genre_table, backref='title_genre')
    tit_keyword = db.relationship('Keyword', secondary=title_keyword_table, backref='title_keyword')
    tit_language = db.Column(db.String, db.ForeignKey('lstLanguage.lng_id'))
    tit_book_main = db.relationship('Book', backref='title_book_main', lazy='dynamic')
    tit_book_sec = db.relationship('Title', secondary=book_title_table, backref='title_book_sec')

    def __repr__(self):
        return "---- Title ----\nid = '%s'\ntitle = '%s'\n" % (self.tit_id, self.tit_title)


class Genre(db.Model):
    __tablename__ = 'lstGenre'

    gnr_id = db.Column(db.String(40), primary_key=True)
    gnr_label = db.Column(db.String(40), nullable=False, unique=True)
    gnr_title = db.relationship('Title', secondary=title_genre_table, backref='genre_title')

    def __repr__(self):
        return "---- Genre ----\nid = '%s'\nlabel = '%s'\n" % (self.gnr_id, self.gnr_label)


class Keyword(db.Model):
    __tablename__ = 'lstKeyword'

    kwd_id = db.Column(db.String(40), primary_key=True)
    kwd_label = db.Column(db.String(40), nullable=False, unique=True)
    kwd_title = db.relationship('Title', secondary=title_keyword_table, backref='keyword_title')

    def __repr__(self):
        return "---- Keyword ----\nid = '%s'\nlabel = '%s'\n" % (self.kwd_id, self.kwd_label)


class Language(db.Model):
    __tablename__ = 'lstLanguage'

    lng_id = db.Column(db.String(40), primary_key=True)
    lng_iso = db.Column(db.String(3))
    lng_label = db.Column(db.String(40), nullable=False)
    lng_title = db.relationship('Title', backref='title_language', lazy='dynamic')

    def __repr__(self):
        return "---- Language ----\nid = '%s'\nlabel = '%s'\n" % (self.lng_id, self.lng_label)


class Book(db.Model):
    __tablename__ = 'tblBook'

    boo_id = db.Column(db.String(40), primary_key=True)
    boo_publisher = db.Column(db.String, db.ForeignKey('lstPublisher.pub_id'))
    boo_main_title = db.Column(db.String, db.ForeignKey('tblTitle.tit_id'))
    boo_subtitle = db.relationship('Title', secondary=book_title_table, backref='book_title_sec')
    book_copy = db.relationship('Copy', backref='book_copy', lazy='dynamic')

    def __repr__(self):
        return "---- Book ----\nid = '%s'\n" % (self.boo_id)


class Copy(db.Model):
    __tablename__ = 'tblCopy'

    cpy_id = db.Column(db.String(40), primary_key=True)
    cpy_isbn13 = db.Column(db.String(13))
    cpy_is_isbn10 = db.Column(db.Boolean)
    cpy_an_edition = db.Column(db.Integer)
    cpy_nb_volumes = db.Column(db.Integer)
    cpy_status = db.Column(db.String(1))
    cpy_comment = db.Column(db.String(250))
    cpy_book = db.Column(db.String, db.ForeignKey('tblBook.boo_id'))
    cpy_shelf = db.Column(db.String, db.ForeignKey('lstShelf.shl_id'))

    def __repr__(self):
        return "---- Copy ----\nid = '%s'\nstatus = '%s'\n" % (self.cpy_id, self.cpy_status)


class Shelf(db.Model):
    __tablename__ = 'lstShelf'

    shl_id = db.Column(db.String(40), primary_key=True)
    shl_label = db.Column(db.String(40), nullable=False, unique=True)
    shl_copy = db.relationship('Copy', backref='shelf_copy', lazy='dynamic')

    def __repr__(self):
        return "---- Shelf ----\nid = '%s'\nlabel = '%s'\n" % (self.shl_id, self.shl_label)


class Publisher(db.Model):
    __tablename__ = 'lstPublisher'

    pub_id = db.Column(db.String(40), primary_key=True)
    pub_label = db.Column(db.String(40), nullable=False, unique=True)
    pub_book = db.relationship('Book', backref='publisher_book', lazy='dynamic')

    def __repr__(self):
        return "---- Publisher ----\nid = '%s'\nlabel = '%s'\n" % (self.pub_id, self.pub_label)
