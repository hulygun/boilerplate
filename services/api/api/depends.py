from typing import Optional

from fastapi import Depends, Header
from i18n import _language

from .db import reset_db_state, db


def get_db(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()


def locale(accept_language: Optional[str] = Header(None)):
    _language.setlocale(accept_language)
    return accept_language