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
        'user_id',
        UUID,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
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
    'games',
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
    Column('esrb_rating', String, nullable=True, unique=False),
)

#######

platforms = Table(
    'platforms',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True
    ),
        Column(
        'platform_name',
        String(100),
        nullable=False,
        unique=True
    ),
        Column(
        'platform_slug',
        String(100),
        nullable=False,
        unique=True
    ),
        Column(
        'platform_name_ru',
        String(100),
        nullable=True
    ),
    Column('code', Integer, nullable=True),
)

game_platforms = Table(
    'game_platforms',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.id', ondelete='CASCADE')
    ),
    Column(
        'platform_id',
        UUID,
        ForeignKey('platforms.id', ondelete='CASCADE')
    ),
    UniqueConstraint('game_id', 'platform_id', name='unique_platform')
)

genres = Table(
    'genres',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True
    ),
    Column(
        'name',
        String(100),
        nullable=False,
        unique=True
    ),
        Column(
        'name_ru',
        String(100),
        nullable=True
    ),
    Column('code', Integer, nullable=True),
)

game_genres = Table(
    'game_genres',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.id', ondelete='CASCADE')
    ),
    Column(
        'genre_id',
        UUID,
        ForeignKey('genres.id', ondelete='CASCADE')
    ),
    UniqueConstraint('game_id', 'genre_id', name='unique_genre')
)


age_ratings = Table(
    'age_ratings',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True
    ),
    Column(
        'type',
        String(100),
        nullable=True,
        unique=True
    ),
        Column(
        'name',
        String(100),
        nullable=False
    ),
    Column('code', Integer, nullable=True),
)

age_rating_games = Table(
    'age_rating_games',
    metadata,
        Column(
        'id',
        UUID,
        primary_key=True
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.id', ondelete='CASCADE')
    ),
    Column(
        'age_rating_id',
        UUID,
        ForeignKey('age_ratings.id', ondelete='CASCADE')
    ),
    UniqueConstraint('game_id', 'age_rating_id', name='unique_age')
)

#######
