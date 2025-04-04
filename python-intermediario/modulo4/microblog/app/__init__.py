import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch
from redis import Redis
import rq
from config import Config


def detect_locale():
    """Detecta e retorna o melhor idioma suportado pelo app."""
    return request.accept_languages.best_match(current_app.config.get('LANGUAGES'))


# Instâncias globais de extensões do Flask
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Você precisa estar logado para acessar esta página.')
mail = Mail()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    """Fábrica de criação do aplicativo Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializando extensões com o app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=detect_locale)

    # Configuração de serviços externos
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config.get('ELASTICSEARCH_URL') else None
    app.redis = Redis.from_url(app.config.get('REDIS_URL', 'redis://'))
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

    # Registro de blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Configuração de logging e monitoramento
    if not app.debug and not app.testing:
        if app.config.get('MAIL_SERVER'):
            auth = (app.config.get('MAIL_USERNAME'), app.config.get('MAIL_PASSWORD')) if app.config.get('MAIL_USERNAME') else None
            secure = () if app.config.get('MAIL_USE_TLS') else None
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=f'no-reply@{app.config["MAIL_SERVER"]}',
                toaddrs=app.config['ADMINS'],
                subject='Microblog - Erro detectado',
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if app.config.get('LOG_TO_STDOUT'):
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            os.makedirs('logs', exist_ok=True)
            file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [em %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog inicializado com sucesso')

    return app


from app import models
