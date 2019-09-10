import os
from flask import Flask

def config():
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config.update(dict(
        DATABASE = os.path.join(app.root_path, 'database.sql'),
        SECRET_KEY = 'development key',
        USERNAME = 'admin',
        PASSWORD = 'default',
    ))
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    return(app)