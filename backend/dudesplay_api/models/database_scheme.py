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
        default=uuid.uuid4(),
        index=True,
    ),
    Column('email', String, unique=True, nullable=False, default=uuid.uuid4()),
    Column('username', String, unique=True, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('name', VARCHAR(255), nullable=False),
    Column('bio', VARCHAR(255), nullable=True),
    Column('profile_picture', String, nullable=True),
    Column('gender', VARCHAR(255), default=None, nullable=True),
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
    Column('game_id', UUID, primary_key=True, default=uuid.uuid4(), index=True),
    Column('title', String, nullable=False),
    Column('cover', String, nullable=True),
    Column('description', String, nullable=True),
    Column('slug', String, nullable=False, unique=True, index=True),
    Column('release', DateTime, nullable=True),
    Column('playtime', Integer, nullable=True, unique=False),
    Column('platform_slug', ARRAY(String), nullable=True, unique=False),
    Column('platforms', ARRAY(String), nullable=True, unique=False),
    Column('parent_platform', ARRAY(String), nullable=True, unique=False),
    Column('genre', ARRAY(String), nullable=True, unique=False),
    Column('tags', ARRAY(String), nullable=True, unique=False),
    Column('avg_rate', Float, nullable=True, unique=False),
    Column('completed_count', Integer, nullable=True, unique=False),
    Column('wishlist_count', Integer, nullable=True, unique=False),
    Column('favorite_count', Integer, nullable=True, unique=False),
    Column('esrb_rating', String, nullable=True, unique=False),
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
        ForeignKey('games.game_id', ondelete='CASCADE'),
    ),
    Column(
        'platform_id',
        UUID,
        ForeignKey('platforms.platform_id', ondelete='CASCADE'),
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
        ForeignKey('games.game_id', ondelete='CASCADE'),
    ),
    Column(
        'genre_id',
        UUID,
        ForeignKey('genres.genre_id', ondelete='CASCADE'),
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

age_rating_games = Table(
    'age_rating_games',
    metadata,
    Column(
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='CASCADE'),
    ),
    Column(
        'age_rating_id',
        UUID,
        ForeignKey('age_ratings.age_rating_id', ondelete='CASCADE'),
    ),
)

#######
game_reviews = Table(
    'game_reviews',
    metadata,
    Column('review_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
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
    Column('list_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
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
        ForeignKey('user_lists.list_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column('added', DateTime(timezone=True)),
)


friends = Table(
    'friends',
    metadata,
    Column(
        'follower_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
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
        default=uuid.uuid4(),
        primary_key=True,
    ),
    Column('is_banned', Boolean, default=False),
    Column('report', String(200), nullable=True),
    Column('created', DateTime(timezone=True)),
    Column('unbanned_day', DateTime(timezone=True)),
    Column('ban_count', Integer),
)

user_settings = Table(
    'user_settings',
    metadata,
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
        primary_key=True,
    ),
    Column('app_theme', Integer, nullable=False),
    Column('delete_request', Boolean, default=False),
    Column('delete_day', DateTime(timezone=True)),
)

user_notifications = Table(
    'user_notifications',
    metadata,
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
        primary_key=True,
    ),
    Column('general', Boolean, default=False),
    Column('updates', Boolean, default=False),
    Column('happy_birthday', Boolean, default=False),
)

user_games = Table(
    'user_games',
    metadata,
    Column('action_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column(
        'game_id',
        UUID,
        ForeignKey('games.game_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column(
        'activity_id',
        UUID,
        ForeignKey('activity_types.activity_id', ondelete='RESTRICT'),
        default=uuid.uuid4(),
    ),
    Column('like_count', Integer, nullable=True),
    Column('user_date', DateTime(timezone=True)),
    Column('created', DateTime(timezone=True)),
)


activity_types = Table(
    'activity_types',
    metadata,
    Column('activity_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)


wall_types = Table(
    'wall_types',
    metadata,
    Column('type_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)

walls = Table(
    'walls',
    metadata,
    Column(
        'wall_id', UUID, primary_key=True, default=uuid.uuid4(),
    ),  # ID профиля или группы, в будущем
    Column('type_id', UUID, ForeignKey('wall_types.type_id', ondelete='RESTRICT')),
    Column(
        'item_id', UUID, nullable=False,
    ),  # ID Элемента, котороый принадлежит этой странице
)

posts = Table(
    'posts',
    metadata,
    Column('post_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column(
        'wall_id',
        UUID,
        ForeignKey('walls.wall_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column(
        'parent_post_id',
        UUID,
        ForeignKey('posts.post_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
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
    Column('tag_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)


post_tags = Table(
    'post_tags',
    metadata,
    Column(
        'post_id',
        UUID,
        ForeignKey('posts.post_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column(
        'tag_id',
        UUID,
        ForeignKey('tags.tag_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
)


post_pictures = Table(
    'post_pictures',
    metadata,
    Column('picture_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column('post_id', UUID, ForeignKey('posts.post_id', ondelete='CASCADE')),
    Column('picture_path', String, nullable=False),
    Column('created', DateTime(timezone=True)),
)


comments = Table(
    'comments',
    metadata,
    Column('comment_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column('item_id', UUID, nullable=False),  # ID то, под чем мы оставляем коммент
    Column(
        'parent_comment_id',
        UUID,
        ForeignKey('comments.comment_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column('like_count', Integer, nullable=True),
    Column('created', DateTime(timezone=True)),

)

like_log = Table(
    'like_log',
    metadata,
    Column('like_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column('post_id', UUID, ForeignKey('like_types.type_id', ondelete='CASCADE')),
    Column('item_id', UUID, nullable=False),  # ID поста, статьи или коммента
    Column(
        'user_id',
        UUID,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        default=uuid.uuid4(),
    ),
    Column('created', DateTime(timezone=True)),
)


like_types = Table(
    'like_types',
    metadata,
    Column('type_id', UUID, primary_key=True, default=uuid.uuid4()),
    Column('name', String(50), nullable=False),
    Column('code', Integer, nullable=True),
)
