import os
basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.abspath(os.path.join(basedir, 'post.db'))

DEBUG = os.environ.get('DEBUG') == 'True'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_dir
SQLALCHEMY_TRACK_MODIFICATIONS = False
