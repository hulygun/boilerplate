from .db import db


from .services.users import models

def create():
    db.connect()
    db.create_tables([models.DBUser])
    db.close()