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
    Column('game_id', UUID, primary_key=True, index=True),
    Column('title', String, nullable=False),
    Column('cover', String, nullable=True),
    Column('description', String, nullable=True),
    Column('slug', String, nullable=False, unique=True, index=True),
    Column('release', DateTime, nullable=True),
    Column('playtime', Integer, nullable=True, unique=False),
    Column('avg_rate', Float, nullable=True, unique=False),
    Column('completed_count', Integer, nullable=True, unique=False),
    Column('wishlist_count', Integer, nullable=True, unique=False),
    Column('favorite_count', Integer, nullable=True, unique=False),
    Column('text_tsv', TSVECTOR, nullable=True, unique=False),
)
Index('my_index', game_table.c.text_tsv, postgresql_using='gin')

#######

platforms = Table(
    'platforms',
    metadata,
    Column(
        'platform_id',
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
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'platform_id',
        UUID,
        ForeignKey('platforms.platform_id', ondelete='CASCADE'), primary_key=True
    ),
    UniqueConstraint('game_id', 'platform_id', name='uix_1')
)


genres = Table(
    'genres',
    metadata,
    Column(
        'genre_id',
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
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'genre_id',
        UUID,
        ForeignKey('genres.genre_id', ondelete='CASCADE'), primary_key=True
    ),
    UniqueConstraint('game_id', 'genre_id', name='uix_2')
)


age_ratings = Table(
    'age_ratings',
    metadata,
    Column(
        'age_rating_id',
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

games_age_ratings = Table(
    'games_age_ratings',
    metadata,
    Column(
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'age_rating_id',
        UUID,
        ForeignKey('age_ratings.age_rating_id', ondelete='CASCADE'), primary_key=True
    ),
    UniqueConstraint('game_id', 'age_rating_id', name='uix_3')
)

#######
game_reviews = Table(
    'game_reviews',
    metadata,
    Column('review_id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'grade',
        Integer,
        CheckConstraint('grade > 0 AND grade < 11'),
    ),
    Column('created', DateTime(timezone=True)),
)


user_lists = Table(
    'user_lists',
    metadata,
    Column('list_id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True
    ),
    Column('name', String(50), nullable=False),
    Column('about', String(140), nullable=True),
    Column('slug', String, nullable=False),
    Column('is_private', Boolean, default=False),
    Column('created', DateTime(timezone=True)),
)


list_games = Table(
    'list_games',
    metadata,
    Column(
        'list_id',
        UUID,
        ForeignKey('user_lists.list_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='CASCADE'), primary_key=True
    ),
    Column('added', DateTime(timezone=True)),
)


friends = Table(
    'friends',
    metadata,
    Column(
        'follower_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True
    ),
    Column('status', Boolean, default=False),
    Column('added', DateTime(timezone=True)),
)

ban_list = Table(
    'ban_list',
    metadata,
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column('is_banned', Boolean, default=False),
    Column('report', String(200), nullable=True),
    Column('created', DateTime(timezone=True)),
    Column('unbanned_day', DateTime(timezone=True)),
    Column('ban_count', Integer),
)

deletion_requests = Table(
    'deletion_requests',
    metadata,
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column('request_day', DateTime(timezone=True)),
    Column('delete_day', DateTime(timezone=True)),
)


mailing_type = Table(
    'mailing_type',
    metadata,
    Column(
        'mailing_id',
        UUID,
        primary_key=True
    ),
    Column(
        'name',
        String(100),
        nullable=False,
        unique=True
    ),
    Column('code', Integer, nullable=True),

)

user_mailing = Table(
    'user_mailing',
    metadata,
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        primary_key=True,
    ),
        Column(
        'mailing_id',
        UUID,
        ForeignKey('mailing_type.mailing_id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column('general', Boolean, default=False),
    Column('updates', Boolean, default=False),
    Column('happy_birthday', Boolean, default=False),
)


user_favorite = Table(
    'user_favorite',
    metadata,
    Column('favorite_id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='RESTRICT'), primary_key=True
    ),
    Column(
        'activity_id',
        UUID,
        ForeignKey('activity_types.activity_id', ondelete='RESTRICT'),
    ),
    Column('like_count', Integer, nullable=True),
    Column('created', DateTime(timezone=True)),
)


user_games = Table(
    'user_games',
    metadata,
    Column('action_id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'activity_id',
        UUID,
        ForeignKey('activity_types.activity_id', ondelete='RESTRICT'), primary_key=True
    ),
    Column('like_count', Integer, nullable=True),
    Column('user_date', DateTime(timezone=True)),
    Column('created', DateTime(timezone=True)),
)


activity_types = Table(
    'activity_types',
    metadata,
    Column('activity_id', UUID, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)


wall_types = Table(
    'wall_types',
    metadata,
    Column('type_id', UUID, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)

walls = Table(
    'walls',
    metadata,
    Column(
        'wall_id', UUID, primary_key=True,
    ),  # ID профиля или группы, в будущем
    Column('type_id', UUID, ForeignKey('wall_types.type_id', ondelete='RESTRICT')),
    Column(
        'item_id', UUID, nullable=False,
    ),  # ID Элемента, котороый принадлежит этой странице
)

posts = Table(
    'posts',
    metadata,
    Column('post_id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'wall_id',
        UUID,
        ForeignKey('walls.wall_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'parent_post_id',
        UUID,
        ForeignKey('posts.post_id', ondelete='CASCADE'), primary_key=True
    ),
    Column('text', String, nullable=False),
    Column('created', DateTime(timezone=True)),
    Column('updated', DateTime(timezone=True)),
    Column('like_count', Integer, nullable=True),
    Column('is_published', Boolean, default=True),
)


tags = Table(
    'tags',
    metadata,
    Column('tag_id', UUID, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)


post_tags = Table(
    'post_tags',
    metadata,
    Column(
        'post_id',
        UUID,
        ForeignKey('posts.post_id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'tag_id',
        UUID,
        ForeignKey('tags.tag_id', ondelete='CASCADE'), primary_key=True
    ),
)


post_pictures = Table(
    'post_pictures',
    metadata,
    Column('picture_id', UUID, primary_key=True),
    Column('post_id', UUID, ForeignKey('posts.post_id', ondelete='CASCADE'), primary_key=True),
    Column('picture_path', String, nullable=False),
    Column('og_picture_path', String, nullable=True),
    Column('created', DateTime(timezone=True)),
)


profile_pictures = Table(
    'profile_pictures',
    metadata,
    Column('picture_id', UUID, primary_key=True),
    Column('user_id', UUID, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True),
    Column('picture_path', String, nullable=False),
    Column('og_picture_path', String, nullable=False),
    Column('created', DateTime(timezone=True)),
)


comments = Table(
    'comments',
    metadata,
    Column('comment_id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True
    ),
    Column('item_id', UUID, nullable=False),  # ID то, под чем мы оставляем коммент
    Column(
        'parent_comment_id',
        UUID,
        ForeignKey('comments.comment_id', ondelete='CASCADE'),
    ),
    Column('like_count', Integer, nullable=True),
    Column('created', DateTime(timezone=True)),

)

like_log = Table(
    'like_log',
    metadata,
    Column('like_id', UUID, primary_key=True),
    Column('type_id', UUID, ForeignKey('like_types.type_id', ondelete='CASCADE'), primary_key=True),
    Column('item_id', UUID, nullable=False, primary_key=True),  # ID поста, статьи или коммента
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
    ),
    Column('created', DateTime(timezone=True)),
)


like_types = Table(
    'like_types',
    metadata,
    Column('type_id', UUID, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)
