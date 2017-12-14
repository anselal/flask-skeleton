import os

from project.server import create_app

from project.server import celery

app = create_app()
celery.conf.update(app.config)
app.app_context().push()