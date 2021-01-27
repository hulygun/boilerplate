import os

DATABASE_NAME = os.getenv('DB_NAME', '../db.sqlite')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_SIGN_DB = 1
REDIS_AUTH_DB = 2

SIGN_EXPIRIES = 60 * 30

SIGN_DOMAIN = os.getenv('SIGN_DOMAIN', '/')