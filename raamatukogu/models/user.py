from raamatukogu import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<User id={} name={!r}>".format(self.id, self.name)
