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

profile_pictures = Table(
    'profile_pictures',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL'), unique=True),
    Column('picture_path', String, unique=False, nullable=False),
    Column('og_picture_path', String, unique=False, nullable=False),
    Column('created', DateTime(timezone=True)),
)

friends = Table(
    'friends',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('follower_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column(
        'status',
        Boolean,
    ),
    Column('added', DateTime(timezone=True)),
)


wall_types = Table(
    'wall_types',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    ),
    Column('name', String, unique=False, nullable=False),
    Column('code', Integer, unique=False, nullable=False),
)

walls = Table(
    'walls',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True,
        default=uuid.uuid4(),
    ),  # ID профиля или группы, в будущем
    Column('type_id', UUID, ForeignKey('wall_types.id', ondelete='RESTRICT')),
    Column(
        'item_id',
        UUID,
        nullable=False,
    ),  # ID Элемента, котороый принадлежит этой странице
)


user_lists = Table(
    'user_lists',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True,
        default=uuid.uuid4(),
    ),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('name', String, unique=False, nullable=False),
    Column('about', String, unique=False, nullable=True),
    Column('is_private', Boolean),
    Column('created', DateTime(timezone=True)),
)


list_games = Table(
    'list_games',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True,
        default=uuid.uuid4(),
    ),
    Column('list_id', UUID, ForeignKey('user_lists.id', ondelete='SET NULL')),
    Column('game_id', UUID, ForeignKey('games.id', ondelete='CASCADE')),
    Column('added', DateTime(timezone=True)),
)


blocked_list = Table(
    'blocked_list',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('is_banned', Boolean),
    Column('report', String),
    Column('ban_count', Integer),
    Column('unbanned_day', DateTime(timezone=True)),
    Column('created', DateTime(timezone=True)),
)


deletion_requests = Table(
    'deletion_requests',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('request_day', DateTime(timezone=True)),
    Column('delete_day', DateTime(timezone=True)),
)

mailing_types = Table(
    'mailing_types',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('name', String, unique=False, nullable=False),
    Column('code', Integer, unique=False, nullable=False),
)


user_mailings = Table(
    'user_mailings',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('mailing_id', UUID, ForeignKey('mailing_types.id', ondelete='SET NULL')),
    Column('created', DateTime(timezone=True)),
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
    Column('completed_count', Integer),
    Column('wishlist_count', Integer),
    Column('favorite_count', Integer),
    Column('average_rating', Float),
    Column('title_tsv', TSVECTOR, nullable=True, unique=False),
)
Index('my_index', game_table.c.title_tsv, postgresql_using='gin')

platforms = Table(
    'platforms',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('platform_name', String(100), nullable=False, unique=True),
    Column('platform_slug', String(100), nullable=False, unique=True),
    Column('platform_name_ru', String(100), nullable=True),
    Column('code', Integer, nullable=True),
)

game_platforms = Table(
    'game_platforms',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('game_id', UUID, ForeignKey('games.id', ondelete='CASCADE')),
    Column('platform_id', UUID, ForeignKey('platforms.id', ondelete='CASCADE')),
    UniqueConstraint('game_id', 'platform_id', name='unique_platform'),
)

genres = Table(
    'genres',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('name', String(100), nullable=False, unique=True),
    Column('name_ru', String(100), nullable=True),
    Column('code', Integer, nullable=True),
)

game_genres = Table(
    'game_genres',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('game_id', UUID, ForeignKey('games.id', ondelete='CASCADE')),
    Column('genre_id', UUID, ForeignKey('genres.id', ondelete='CASCADE')),
    UniqueConstraint('game_id', 'genre_id', name='unique_genre'),
)


age_ratings = Table(
    'age_ratings',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('type', String(100), nullable=True, unique=True),
    Column('name', String(100), nullable=False),
    Column('code', Integer, nullable=True),
)

age_rating_games = Table(
    'age_rating_games',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('game_id', UUID, ForeignKey('games.id', ondelete='CASCADE')),
    Column('age_rating_id', UUID, ForeignKey('age_ratings.id', ondelete='CASCADE')),
    UniqueConstraint('game_id', 'age_rating_id', name='unique_age'),
)

activity_types = Table(
    'activity_types',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('name', String, unique=False, nullable=False),
    Column('code', Integer, unique=False, nullable=False),
)

user_favorite = Table(
    'user_favorite',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('game_id', UUID, ForeignKey('games.id', ondelete='CASCADE')),
    Column('activity_id', UUID, ForeignKey('activity_types.id', ondelete='SET NULL')),
    Column('created', DateTime(timezone=True)),
    Column('like_count', Integer),
)


user_games = Table(
    'user_games',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('game_id', UUID, ForeignKey('games.id', ondelete='CASCADE')),
    Column('activity_id', UUID, ForeignKey('activity_types.id', ondelete='SET NULL')),
    Column('created', DateTime(timezone=True)),
    Column('like_count', Integer),
)


game_reviews = Table(
    'game_reviews',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('game_id', UUID, ForeignKey('games.id', ondelete='CASCADE')),
    Column('created', DateTime(timezone=True)),
    Column('grade', Integer),
)


posts = Table(
    'posts',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('wall_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('parent_post_id', UUID, ForeignKey('posts.id', ondelete='CASCADE')),
    Column('text', String, nullable=False),
    Column('created', DateTime(timezone=True)),
    Column('updated', DateTime(timezone=True)),
    Column('like_count', Integer),
    Column('is_published', Boolean),
)


tags = Table(
    'tags',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('name', String, unique=False, nullable=False),
    Column('code', Integer, unique=False, nullable=False),
)


content_tags = Table(
    'content_tags',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('content_id', UUID, unique=False, nullable=False),
    Column('tag_id', UUID, ForeignKey('tags.id', ondelete='SET NULL')),
)

articles = Table(
    'articles',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('wall_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('parent_post_id', UUID, ForeignKey('articles.id', ondelete='CASCADE')),
    Column('title', String, nullable=False),
    Column('content', String, nullable=False),
    Column('created', DateTime(timezone=True)),
    Column('updated', DateTime(timezone=True)),
    Column('like_count', Integer),
    Column('slug', String, nullable=False),
    Column('is_published', Boolean),
)


content_pictures = Table(
    'content_pictures',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('content_id', UUID, unique=False, nullable=False),
    Column('picture_path', String, unique=False, nullable=False),
    Column('og_picture_path', String, unique=False, nullable=False),
    Column('created', DateTime(timezone=True)),
)


comments = Table(
    'comments',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('content_id', UUID, unique=False, nullable=False),
    Column(
        'parent_comment_id', UUID, ForeignKey('comments.id', ondelete='SET NULL')
    ),  # на случай, если комментарий является ответом
    Column('created', DateTime(timezone=True)),
    Column('updated', DateTime(timezone=True)),
    Column('like_count', Integer),
)


like_types = Table(
    'like_types',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('name', String, unique=False, nullable=False),
    Column('code', Integer, unique=False, nullable=False),
)


like_log = Table(
    'like_log',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='SET NULL')),
    Column('content_id', UUID, unique=False, nullable=False),
    Column(
        'type_id', UUID, ForeignKey('like_types.id', ondelete='SET NULL')
    ),  # на случай, если комментарий является ответом
    Column('value', Boolean),
    Column('created', DateTime(timezone=True)),
)
