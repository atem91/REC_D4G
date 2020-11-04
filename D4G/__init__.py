from flask import Flask

from .views import app, db, init_db
#from . import models

# Connect sqlalchemy to app
db.init_app(app)

@app.cli.command()
def init_db2():
    init_db()