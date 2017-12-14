import unittest
import coverage

from flask_migrate import Migrate

from project.server import create_app, db

app = create_app()
migrate = Migrate(app, db)

# code coverage
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()


@app.cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@app.cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@app.cli.command()
def create_db():
    """Creates the db tables."""
    db.create_all()


@app.cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@app.cli.command()
def create_admin():
    """Creates the admin user."""
    from project.server.models import User

    db.session.add(User(email='ad@min.com', password='admin', admin=True))
    db.session.commit()