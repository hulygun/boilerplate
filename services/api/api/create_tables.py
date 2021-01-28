from .db import db


from .services.users.models import DBUser

MODELS = [DBUser]

def create():
    db.connect()
    db.create_tables(MODELS)
    db.close()