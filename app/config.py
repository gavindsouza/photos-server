import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	STATIC_FOLDER = os.path.join(os.pardir, 'static/dist')
	HOST = '0.0.0.0'

class DevelopmentConfig(Config):
	DEBUG = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key_here'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig
}
