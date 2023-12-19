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
    'games',
    metadata,
    Column('id', UUID, primary_key=True, index=True, unique=True,),
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
    Column('title_tsv', TSVECTOR, nullable=True, unique=False),
)
Index('game_index', game_table.c.title_tsv, postgresql_using='gin')


dlc_table = Table(
    'dlc',
    metadata,
    Column('id', UUID, primary_key=True, index=True),
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
    Column('title_tsv', TSVECTOR, nullable=True, unique=False),
)
Index('dlc_index', dlc_table.c.title_tsv, postgresql_using='gin')


game_dlc = Table(
    'games_dlc',
    metadata,
    Column('id', UUID, primary_key=True, index=True),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.id', ondelete='CASCADE')
    ),
    Column(
        'dlc_id',
        UUID,
        ForeignKey('dlc.id', ondelete='CASCADE')
    ),
    UniqueConstraint('game_id', 'dlc_id', name='unique_dlc')
)


gaming_platforms = Table(
    'gaming_platforms',
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
        ForeignKey('gaming_platforms.id', ondelete='CASCADE')
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
        'type', #pegi, rars, esrb, iarc
        String(50),
        nullable=False,
        unique=False
    ),
    Column(
        'name',
        String(100),
        nullable=False,
        unique=True
    ),
    Column('code', Integer, nullable=True),


)

age_ratings_games = Table(
    'age_ratings_games',
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
    UniqueConstraint('game_id', 'age_rating_id', name='unique_age_ratings_games')
)


game_reviews = Table(
    'game_reviews',
    metadata,
    Column('id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE')
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.id', ondelete='CASCADE')
    ),
    Column(
        'grade',
        Integer,
        CheckConstraint('grade > 0 AND grade < 11'),
    ),
    Column('created', DateTime(timezone=True)),
    UniqueConstraint('user_id', 'game_id', name='one_review_one_user')
)


user_lists = Table(
    'user_lists',
    metadata,
    Column('id', UUID, primary_key=True),
    Column(
        'owner_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE')
    ),
    Column(
        'added_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE')
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
        'id',
        UUID,
        primary_key=True
    ),
    Column(
        'list_id',
        UUID,
        ForeignKey('user_lists.id', ondelete='CASCADE'), primary_key=True
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.id', ondelete='CASCADE'), primary_key=True
    ),
    Column('added', DateTime(timezone=True)),
    UniqueConstraint('list_id', 'game_id', name='one_list_one_game')

)


friends = Table(
    'friends',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True
    ),
    Column(
        'follower_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE')
    ),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE')
    ),
    Column('status', Boolean, default=False),
    Column('added', DateTime(timezone=True)),
    UniqueConstraint('follower_id', 'user_id', name='one_relationship')

)

ban_list = Table(
    'ban_list',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True
    ),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE'),
    ),
    Column(
        'admin_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE'),
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
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column('request_day', DateTime(timezone=True)),
    Column('delete_day', DateTime(timezone=True)),
)


mailing_type = Table(
    'mailing_type',
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
    Column('code', Integer, nullable=True),

)

user_mailing = Table(
    'user_mailing',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True
                ),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE'),
    ),
        Column(
        'mailing_id',
        UUID,
        ForeignKey('mailing_type.id', ondelete='CASCADE'),
    ),
    Column('general', Boolean, default=False),
    Column('updates', Boolean, default=False),
    Column('happy_birthday', Boolean, default=False),
)


user_favorite = Table(
    'user_favorite',
    metadata,
    Column('id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE')
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.id', ondelete='RESTRICT')
    ),
    Column(
        'activity_id',
        UUID,
        ForeignKey('activity_types.id', ondelete='RESTRICT'),
    ),
    Column('like_count', Integer, nullable=True),
    Column('created', DateTime(timezone=True)),
)


user_games = Table(
    'user_games',
    metadata,
    Column('id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE')
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.id', ondelete='CASCADE')
    ),
    Column(
        'activity_id',
        UUID,
        ForeignKey('activity_types.id', ondelete='RESTRICT')
    ),
    Column('like_count', Integer, nullable=True),
    Column('user_date', DateTime(timezone=True)),
    Column('created', DateTime(timezone=True)),
)


activity_types = Table(
    'activity_types',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)


wall_types = Table(
    'wall_types',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)

walls = Table(
    'walls',
    metadata,
    Column(
        'id', UUID, primary_key=True,
    ),  # ID профиля или группы, в будущем
    Column('type_id', UUID, ForeignKey('wall_types.id', ondelete='RESTRICT')),
    Column(
        'item_id', UUID, nullable=False,
    ),  # ID Элемента, котороый принадлежит этой странице
)

posts = Table(
    'posts',
    metadata,
    Column('id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE')
    ),
    Column(
        'wall_id',
        UUID,
        ForeignKey('walls.id', ondelete='CASCADE')
    ),
    Column(
        'parent_post_id',
        UUID,
        ForeignKey('posts.id', ondelete='CASCADE')
    ),
    Column('text', String, nullable=True),
    Column('created', DateTime(timezone=True)),
    Column('updated', DateTime(timezone=True)),
    Column('like_count', Integer, nullable=True),
    Column('is_published', Boolean, default=True),
)


tags = Table(
    'tags',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)


post_tags = Table(
    'post_tags',
    metadata,
    Column(
        'id',
        UUID,
        primary_key=True,
    ),
    Column(
        'post_id',
        UUID,
        ForeignKey('posts.id', ondelete='CASCADE')
    ),
    Column(
        'tag_id',
        UUID,
        ForeignKey('tags.id', ondelete='CASCADE')
    ),
    UniqueConstraint('post_id', 'tag_id', name='only_unique_tag')

)


post_pictures = Table(
    'post_pictures',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('post_id', UUID, ForeignKey('posts.id', ondelete='CASCADE')),
    Column('picture_path', String, nullable=False),
    Column('og_picture_path', String, nullable=True),
    Column('created', DateTime(timezone=True)),
)


profile_pictures = Table(
    'profile_pictures',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('user_id', UUID, ForeignKey('users.id', ondelete='CASCADE')),
    Column('picture_path', String, nullable=False),
    Column('og_picture_path', String, nullable=False),
    Column('created', DateTime(timezone=True)),
)


comment_log = Table(
    'comments',
    metadata,
    Column('id', UUID, primary_key=True),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE')
    ),
    Column('content_id', UUID, nullable=False),  # ID то, под чем мы оставляем коммент
    Column(
        'parent_comment_id',
        UUID,
        ForeignKey('comments.id', ondelete='CASCADE'),
    ),
    Column('like_count', Integer, nullable=True),
    Column('created', DateTime(timezone=True)),

)

like_log = Table(
    'like_log',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('type_id', UUID, ForeignKey('like_types.id', ondelete='CASCADE')), #чему мы ставим лайк (коммент, пост или что-то еще)
    Column('content_id', UUID, nullable=False),  # ID поста, статьи или коммента
    Column(
        'user_id',
        UUID,
        ForeignKey('users.id', ondelete='CASCADE'),
    ),
    Column('created', DateTime(timezone=True)),
)


like_types = Table(
    'like_types',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)
