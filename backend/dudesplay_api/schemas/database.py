import uuid

from sqlalchemy import (
    ARRAY,
    UUID,
    VARCHAR,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()


user_table = Table(
    'users',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
        default=uuid.uuid4
    ),
    Column('email', String, unique=True, nullable=False),
    Column('username', String, unique=True, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('name', String(255), nullable=False),
    Column('bio', String(255), nullable=True),
    Column('gender', String(255), default=None, nullable=True),
    Column('birthdate', Date, default=None, nullable=True),
    Column('is_verified', Boolean, default=False),
    Column('is_superuser', Boolean, default=False),
    Column('is_writer', Boolean, default=False),
    Column('official_person', Boolean, default=False),
    Column('registration_date', DateTime(timezone=True)),
)


game_table = Table(
    'game',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('title', String, nullable=False),
    Column('cover', String, nullable=True),
    Column('description', String, nullable=True),
    Column('slug', String, nullable=False, unique=True, index=True),
    Column('release', DateTime, nullable=True),
    Column('playtime', Integer, nullable=True, unique=False),
    Column('platform', ARRAY(String), nullable=True, unique=False),
    Column('platform_name', ARRAY(String), nullable=True, unique=False),
    Column('parent_platform', ARRAY(String), nullable=True, unique=False),
    Column('genre', ARRAY(String), nullable=True, unique=False),
    Column('tags', ARRAY(String), nullable=True, unique=False),
    Column('esrb_rating', String, nullable=True, unique=False),
)
