import re
import unicodedata
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from app.models.post import Post


def slugify(text: str) -> str:
    """Convert a string to a URL-friendly slug."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


class PostForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(), Length(min=5, max=150, message='Title must be between 5 and 150 characters.')
    ])
    slug = StringField('URL Slug', validators=[
        Optional(), Length(max=180)
    ])
    summary = TextAreaField('Summary / Excerpt', validators=[
        Optional(), Length(max=300, message='Summary must be under 300 characters.')
    ])
    content = HiddenField('Content', validators=[
        DataRequired(message='Post content cannot be empty.')
    ])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    tags = StringField('Tags', validators=[Optional(), Length(max=200)],
                       description='Comma-separated tags, e.g. Flask, Python, Web')
    published = BooleanField('Publish immediately', default=True)
    submit = SubmitField('Save Post')

    def __init__(self, *args, original_slug=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_slug = original_slug

    def validate_slug(self, field):
        if field.data:
            slug = slugify(field.data)
            existing = Post.query.filter_by(slug=slug).first()
            if existing and slug != self.original_slug:
                raise ValidationError('This slug is already in use. Try a different title or slug.')


class CommentForm(FlaskForm):
    body = TextAreaField('Leave a Comment', validators=[
        DataRequired(message='Comment cannot be empty.'),
        Length(min=2, max=1000, message='Comment must be between 2 and 1000 characters.')
    ])
    submit = SubmitField('Post Comment')
