import uuid

from sqlalchemy import UUID, Column, MetaData, String, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column(
        "id", UUID, primary_key=True, unique=True, nullable=False, default=uuid.uuid4()
    ),
    Column("email", String, unique=True),
    Column("username", String, unique=True),
    Column("hashed_password", String),
)
