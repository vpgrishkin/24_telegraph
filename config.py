import os
basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.abspath(os.path.join(basedir, 'post.db'))

class Config(object):
    # CSRF_ENABLED = True
    # WTF_CSRF_SECRET_KEY = 'dsofpkoasodksap'
    # SECRET_KEY = 'zxczxasdsad'
    # CSRF_ENABLED = True
    # SECRET_KEY = 'fdaskfsdlfkfasdkfmsd432423rdf'

    DEBUG = os.environ.get('DEBUG') == 'True'
    PORT = int(os.environ.get('PORT', 5000))
    

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + db_dir
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = True

class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
