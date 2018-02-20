from flask import Flask 
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
# login_manager.login_view = <path to login view function>


def create_app(config_name):
	"""Factory function to create app instances."""
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)
	login_manager.init_app(app)

	if app.config['SSL_REFIRECT']:
		from flask_sslify import SSLify
		sslify = SSLify(app)

	# Register blueprints here
	from app.main import main
	app.register_blueprint(main, url_prefix='/main')

	return app