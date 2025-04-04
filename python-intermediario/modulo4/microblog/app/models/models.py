from datetime import datetime, timezone
from hashlib import md5
from time import time
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from app.search import add_to_index, remove_from_index, query_index


class SearchMixin:
    @classmethod
    def search(cls, query_text, page, per_page):
        item_ids, total_items = query_index(cls.__tablename__, query_text, page, per_page)
        if not total_items:
            return [], 0
        order_map = {item_id: idx for idx, item_id in enumerate(item_ids)}
        result_query = sa.select(cls).where(cls.id.in_(item_ids)).order_by(db.case(order_map, value=cls.id))
        return db.session.scalars(result_query), total_items

    @classmethod
    def handle_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def post_commit(cls, session):
        for action, items in session._changes.items():
            for item in items:
                if isinstance(item, SearchMixin):
                    if action == 'add' or action == 'update':
                        add_to_index(item.__tablename__, item)
                    elif action == 'delete':
                        remove_from_index(item.__tablename__, item)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in db.session.scalars(sa.select(cls)):
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchMixin.handle_commit)
db.event.listen(db.session, 'after_commit', SearchMixin.post_commit)

followers_table = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers_table, primaryjoin=(followers_table.c.follower_id == id),
        secondaryjoin=(followers_table.c.followed_id == id), back_populates='followers'
    )
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers_table, primaryjoin=(followers_table.c.followed_id == id),
        secondaryjoin=(followers_table.c.follower_id == id), back_populates='following'
    )

    def __str__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_avatar(self, size):
        hash_digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{hash_digest}?d=identicon&s={size}'

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return db.session.scalar(self.following.select().where(User.id == user.id)) is not None

    def count_followers(self):
        return db.session.scalar(sa.select(sa.func.count()).select_from(self.followers.select().subquery()))

    def count_following(self):
        return db.session.scalar(sa.select(sa.func.count()).select_from(self.following.select().subquery()))

    def followed_posts(self):
        Author = so.aliased(User)
        return (
            sa.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(User), isouter=True)
            .where(sa.or_(User.id == self.id, Author.id == self.id))
            .order_by(Post.timestamp.desc())
        )

    def generate_reset_token(self, expiration=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expiration}, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def validate_reset_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except Exception:
            return None
        return db.session.get(User, user_id)


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Post(SearchMixin, db.Model):
    __searchable__ = ['body']
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5))

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __str__(self):
        return f'<Post {self.body}>'
