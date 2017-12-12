# project/server/__init__.py


import os

from flask import Flask, render_template

from project.server.celery import make_celery
from project.server.extensions import login_manager, toolbar, bootstrap, db, migrate, mail, socketio

import eventlet
eventlet.monkey_patch()

# instantiate the app
app = Flask(
    __name__,
    template_folder='../client/templates',
    static_folder='../client/static'
)


# set config
app_settings = os.getenv(
'APP_SETTINGS', 'project.server.config.DevelopmentConfig')
app.config.from_object(app_settings)


# set up extensions
login_manager.init_app(app)
toolbar.init_app(app)
bootstrap.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)
socketio.init_app(app, message_queue='redis://', async_mode='eventlet')
celery = make_celery(app)


# register blueprints
from project.server.user.views import user_blueprint
from project.server.main.views import main_blueprint
app.register_blueprint(user_blueprint)
app.register_blueprint(main_blueprint)


# flask login
from project.server.models import User
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


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

