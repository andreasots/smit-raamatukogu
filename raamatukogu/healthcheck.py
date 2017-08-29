import flask
import sqlalchemy as sa
from sqlalchemy.sql.expression import func

from raamatukogu import app, db

__all__ = ['blueprint']

blueprint = flask.Blueprint('healthcheck', __name__)

@blueprint.route("/healthcheck")
def healthcheck():
    try:
        in_recovery, = db.engine.execute(sa.select([func.pg_is_in_recovery()])).first()
        if in_recovery:
            raise Exception("Database is in recovery")
    except Exception as e:
        return flask.jsonify(
            errors=[
                {
                    "status": 503,
                    "title": "Service Unavailable",
                    "detail": str(e),
                }
            ]
        ), 503

    return "", 204
