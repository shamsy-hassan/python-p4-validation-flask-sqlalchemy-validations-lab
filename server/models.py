from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")
        
        existing_author = Author.query.filter(Author.name == name).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError("Author name must be unique.")
        
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number:
            if len(phone_number) != 10 or not phone_number.isdigit():
                raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'<Author id={self.id}, name={self.name}>'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title.")
        
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in clickbait_words):
            raise ValueError("Title must be clickbait-y.")
        
        return title

    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary must be maximum 250 characters long.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Fiction', 'Non-Fiction']
        if category not in valid_categories:
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        return category

    def __repr__(self):
        return f'<Post id={self.id}, title={self.title}>'
