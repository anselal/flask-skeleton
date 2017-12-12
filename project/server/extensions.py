from flask_login import LoginManager
login_manager = LoginManager()

from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension()

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_migrate import Migrate
migrate = Migrate()

from flask_mail import Mail
mail = Mail()

from flask_socketio import SocketIO
socketio = SocketIO()
