import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(32)



class DevelopmentConfig(Config):
    POSTGRES = {
        'user': 'postgres',
        'pw': '1',
        'db': 'jto',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    POSTGRES = {
        'user': 'postgres',
        'pw': '!J.0.0.0',
        'db': 'jtodb',
        'host': 'jto-instance.cwa9qfrslztl.us-west-2.rds.amazonaws.com',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
