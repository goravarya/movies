from settings import debug, db_name


# FixMe: It does not seem the ideal way of storing configs.
class Config:
    def __init__(self):
        pass

    DEBUG = debug
    SQLALCHEMY_ECHO = debug
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/gorav/python/db/' + db_name + '.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
