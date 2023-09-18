import uuid

from sqlalchemy import UUID, Boolean, Column, Date, MetaData, String, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column(
        "id", UUID, primary_key=True, unique=True, nullable=False, default=uuid.uuid4()
    ),
    Column("email", String, unique=True, nullable=False, default=uuid.uuid4()),
    Column("username", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("name", String, nullable=False),
    Column("surname", String, default=None, nullable=True),
    Column("img", String, default=None, nullable=True),
    Column("sex", String, default=None, nullable=True),
    Column("birthdate", Date, default=None, nullable=True),
    Column("is_verified", Boolean, default=False),
    Column("is_superuser", Boolean, default=False),
    Column("is_writer", Boolean, default=False),
)
