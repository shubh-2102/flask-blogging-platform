import os
from app import create_app, db
from app.models import User, Post, Category, Tag, Comment

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
