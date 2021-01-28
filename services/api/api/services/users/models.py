from datetime import datetime

import peewee
from pytz import UTC

from api.db import db


class DBUser(peewee.Model):
    id = peewee.UUIDField(primary_key=True)
    email = peewee.CharField(unique=True, index=True)
    password = peewee.CharField(null=True)
    is_active = peewee.BooleanField(default=False)
    created = peewee.DateTimeField(default=datetime.now(tz=UTC))

    class Meta:
        database = db
        table_name = 'users'