from .base import *  # noqa
import os

SQLALCHEMY_DATABASE_URI = os.getenv("SUPABASE_TEST_DB_URL")
TESTING = True