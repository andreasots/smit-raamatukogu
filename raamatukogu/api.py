import flask

from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields

from raamatukogu import app, db
from raamatukogu.models import Book, Loan, User

__all__ = ['blueprint']

blueprint = flask.Blueprint('api', __name__)

class UserSchema(Schema):
    class Meta:
        type_ = 'user'
        self_view = 'api.user_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.user_list'

    id = fields.Str(dump_only=True)
    name = fields.Str(requried=True)

class UserList(ResourceList):
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User,
    }

class UserDetail(ResourceDetail):
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User,
    }

class BookSchema(Schema):
    class Meta:
        type_ = 'book'
        self_view = 'api.book_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.book_list'

    id = fields.Str(dump_only=True)
    title = fields.Str(requried=True)
    author = fields.Str(requried=True)

class BookList(ResourceList):
    schema = BookSchema
    data_layer = {
        'session': db.session,
        'model': Book,
    }

class BookDetail(ResourceDetail):
    schema = BookSchema
    data_layer = {
        'session': db.session,
        'model': Book,
    }

class LoanSchema(Schema):
    class Meta:
        type_ = 'loan'
        self_view = 'api.loan_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.loan_list'

    id = fields.Str(dump_only=True)
    borrower = Relationship(
        attribute='user',
        self_view='api.loan_borrower',
        self_view_kwargs={'id': '<id>'},
        related_view='api.user_detail',
        related_view_kwargs={'id': '<id>'},
        schema=UserSchema,
        type_='user',
    )
    book = Relationship(
        self_view='api.loan_book',
        self_view_kwargs={'id': '<id>'},
        related_view='api.book_detail',
        related_view_kwargs={'id': '<id>'},
        schema=BookSchema,
        type_='book',
    )

class LoanList(ResourceList):
    schema = LoanSchema
    data_layer = {
        'session': db.session,
        'model': Loan,
    }

class LoanDetail(ResourceDetail):
    schema = LoanSchema
    data_layer = {
        'session': db.session,
        'model': Loan,
    }

class LoanBorrower(ResourceRelationship):
    schema = LoanSchema
    data_layer = {
        'session': db.session,
        'model': Loan,
    }

class LoanBook(ResourceRelationship):
    schema = LoanSchema
    data_layer = {
        'session': db.session,
        'model': Loan,
    }

api = Api(app, blueprint)

api.route(UserList, 'user_list', '/users')
api.route(UserDetail, 'user_detail', '/users/<int:id>')
api.route(BookList, 'book_list', '/books')
api.route(BookDetail, 'book_detail', '/books/<int:id>')
api.route(LoanList, 'loan_list', '/loans')
api.route(LoanDetail, 'loan_detail', '/loans/<int:id>')
api.route(LoanBorrower, 'loan_borrower', '/loans/<int:id>/relationships/borrower')
api.route(LoanBook, 'loan_book', '/loans/<int:id>/relationships/book')
