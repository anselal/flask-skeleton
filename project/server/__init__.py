# project/server/__init__.py


import os
import project.server.filters

from flask import Flask, render_template

from project.server.celery import make_celery
from project.server.extensions import login_manager, toolbar, bootstrap, db, migrate, mail, socketio

import eventlet
eventlet.monkey_patch()


def create_app(app_name=__name__, config=None):

    # instantiate the app
    app = Flask(
        app_name,
        template_folder='../client/templates',
        static_folder='../client/static'
    )

    configure_app(app, config)
    configure_blueprints(app)
    configure_extensions(app)
    configure_template_filters(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config=None):
    # set config
    app_settings = os.getenv(
        'APP_SETTINGS', 'project.server.config.DevelopmentConfig')
    app.config.from_object(app_settings)

    if config:
        app.config.from_object(config)


def configure_extensions(app):

    # DebugToolbar
    toolbar.init_app(app)

    # Bootstrap
    bootstrap.init_app(app)

    # SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    # Flask-Mail
    mail.init_app(app)

    # Flask-SocketIO
    socketio.init_app(app, message_queue='redis://', async_mode='eventlet')

    # Celery
    celery = make_celery(app)

    # Flask-Login
    login_manager.init_app(app)

    from project.server.models import User
    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def configure_blueprints(app):

    from project.server.user.views import user_blueprint
    from project.server.main.views import main_blueprint

    for bp in [user_blueprint, main_blueprint]:
        app.register_blueprint(bp)


def configure_template_filters(app):

    import inspect

    # Register all filters in filters file
    for f in filter(lambda f: inspect.isfunction(getattr(project.server.filters, f)), dir(project.server.filters)):
        app.jinja_env.filters[f] = getattr(project.server.filters, f)


def configure_error_handlers(app):

    # error handlers
    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500

