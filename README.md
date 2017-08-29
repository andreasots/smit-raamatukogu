# smit-raamatukogu

Time spent: 8h

## Setup

Adjust `sqlalchemy.url` in `alembic.ini` to point to a PostgreSQL database.
The default is `postgresql:///smit-raamatukogu`.

```
$ virtualenv venv --python python3
$ . venv/bin/activate
$ pip install -r requirements.txt
$ alembic upgrade head
```

## Start debug server

```
$ python3 start.py
```

## Run integration tests

This requires a running server. Use the `--base-url` argument to run the tests
against a server other than the debug server.

```
$ pytest
```
