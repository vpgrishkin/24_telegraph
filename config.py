import os
basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.abspath(os.path.join(basedir, 'post.db'))

DEBUG = os.environ.get('DEBUG') == 'True'
PORT = int(os.environ.get('PORT', 5000))


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_dir
SQLALCHEMY_TRACK_MODIFICATIONS = False
