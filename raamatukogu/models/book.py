from raamatukogu import db

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Book id={} title={!r} author={!r}>".format(self.id, self.title, self.author)