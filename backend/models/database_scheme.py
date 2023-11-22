import datetime
import uuid

from sqlalchemy import UUID, Boolean, Column, Date, MetaData, String, Table, VARCHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("user_id", UUID, primary_key=True, unique=True, nullable=False, default=uuid.uuid4(), index=True),
    Column("email", String, unique=True, nullable=False, default=uuid.uuid4()),
    Column("username", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("name", VARCHAR(255), nullable=False),
    Column("bio", VARCHAR(255), nullable=True),
    Column("profile_picture", String, nullable=True),
    Column("gender", VARCHAR(255), default=None, nullable=True),
    Column("birthdate", Date, default=None, nullable=True),
    Column("is_verified", Boolean, default=False),
    Column("is_superuser", Boolean, default=False),
    Column("is_writer", Boolean, default=False),
    Column("registration_date", DateTime(timezone=True))
)
