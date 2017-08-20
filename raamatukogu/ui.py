import flask

__all__ = ['blueprint']

blueprint = flask.Blueprint('ui', __name__)

@blueprint.route('/')
def index():
    return flask.render_template('index.html')
