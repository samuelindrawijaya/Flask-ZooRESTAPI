from .base import *  # noqa
import os
SQLALCHEMY_DATABASE_URI = os.getenv("SUPABASE_DB_URL")  # Supabase PostgreSQL URL
