import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY', "some-random-string")
	SSL_REDIRECT = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db.sqlite3")


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.sqlite3")
	WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

	@classmethod
	def init_app(cls, app):
		Config.init_app(app)


class HerokuConfig(ProductionConfig):
	SSL_REDIRECT = True if os.environ.get('DYNO') else False

	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)

		# handle reverse proxy server headers
		from werkzeug.contrib.fixers import ProxyFix
		app.wsgi_app = ProxyFix(app.wsgi_app)

		# log to stderr
		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.INFO)
		app.logger.add_handler(file_handler)


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'heroku': HerokuConfig,
	'default': DevelopmentConfig
}