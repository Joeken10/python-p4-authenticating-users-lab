from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Define naming conventions for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Article(db.Model, SerializerMixin):
    """Model representing an article."""

    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))  # Specify length
    title = db.Column(db.String(200), nullable=False)  # Specify length and make non-nullable
    content = db.Column(db.Text, nullable=False)  # Use Text for longer content
    preview = db.Column(db.String(300))  # Specify length for preview
    minutes_to_read = db.Column(db.Integer, default=0)  # Set default value
    date = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Article {self.id} by {self.author}>'

    def to_dict(self):
        """Convert the Article instance to a dictionary format."""
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'content': self.content,
            'preview': self.preview,
            'minutes_to_read': self.minutes_to_read,
            'date': self.date.isoformat() if self.date else None,
            'user_id': self.user_id
        }


class User(db.Model, SerializerMixin):
    """Model representing a user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # Make username non-nullable and specify length
    name = db.Column(db.String(100), nullable=False)  # Specify length and make non-nullable

    articles = db.relationship('Article', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}, Name: {self.name}, ID: {self.id}>'

    def to_dict(self):
        """Convert the User instance to a dictionary format."""
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'articles': [article.to_dict() for article in self.articles]  # Include related articles
        }
