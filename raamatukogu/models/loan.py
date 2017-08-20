from raamatukogu import db

class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.BigInteger, db.ForeignKey('books.id'), nullable=False)

    user = db.relationship('User', foreign_keys=[user_id])
    book = db.relationship('Book', foreign_keys=[book_id])

    def __repr__(self):
        return "<Loan user_id={} book_id={} due_date={}>".format(self.id, self.user_id, self.book_id, self.due_date)