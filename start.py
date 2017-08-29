from raamatukogu import app
import raamatukogu.ui
import raamatukogu.api
import raamatukogu.healthcheck

__all__ = ['app']

app.register_blueprint(raamatukogu.ui.blueprint)
app.register_blueprint(raamatukogu.api.blueprint, url_prefix="/api/v1")
app.register_blueprint(raamatukogu.healthcheck.blueprint, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)
else:
    import logging
    app.logger.addHandler(logging.StreamHandler())
