import datetime
import uuid

from sqlalchemy import ARRAY, CHAR, UUID, Boolean, Column, Date, ForeignKey, Integer, MetaData, String, Table, VARCHAR, DateTime, FLOAT, CheckConstraint
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
    Column("official_person", Boolean, default=False),
    Column("registration_date", DateTime(timezone=True))
)


game_table = Table(
    'games',
    metadata,
    Column('game_id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
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
    Column('avg_rate', FLOAT, nullable=True, unique=False),
    Column('completed_count', Integer, nullable=True, unique=False),
    Column('wishlist_count', Integer, nullable=True, unique=False),
    Column('favorite_count', Integer, nullable=True, unique=False),
    Column('esrb_rating', String, nullable=True, unique=False),
)

game_reviews = Table(
    'game_reviews',
    metadata,
    Column('review_id',UUID, primary_key=True, default=uuid.uuid4()),
    Column('user_id', UUID, ForeignKey('users.user_id', ondelete="CASCADE"), default=uuid.uuid4()),
    Column('game_id', UUID, ForeignKey('games.game_id', ondelete="CASCADE"), default=uuid.uuid4()),
    Column('grade', Integer, CheckConstraint('grade > 0 AND grade < 11'), ),
    Column('text', CHAR(140), nullable=True),
    Column('like_count', Integer, nullable=True),
    Column("created", DateTime(timezone=True))
)


user_lists = Table(
    'user_lists',
    metadata,
    Column('list_id',UUID, primary_key=True, default=uuid.uuid4()),
    Column('user_id', UUID, ForeignKey('users.user_id', ondelete="CASCADE"), default=uuid.uuid4()),
    Column('name', CHAR(50), nullable=False),
    Column('about', CHAR(140), nullable=True),
    Column('slug', CHAR, nullable=False),
    Column("is_private", Boolean, default=False),
    Column("created", DateTime(timezone=True))
)

list_games = Table(
    'list_games',
    metadata,
    Column('list_id', UUID, ForeignKey('user_lists.list_id', ondelete="CASCADE"), default=uuid.uuid4()),
    Column('user_id', UUID, ForeignKey('users.user_id', ondelete="CASCADE"), default=uuid.uuid4()),
    Column('name', CHAR(50), nullable=False),
    Column('about', CHAR(140), nullable=True),
    Column('slug', CHAR, nullable=False),
    Column("is_private", Boolean, default=False),
    Column("created", DateTime(timezone=True))
)