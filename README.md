# Flask Skeleton

Flask starter project...

[![Build Status](https://travis-ci.org/realpython/flask-skeleton.svg?branch=master)](https://travis-ci.org/realpython/flask-skeleton)

## Quick Start

### Basics

Create virtual environment and install requirements via pipenv extension
Enter everything without double slashes

```sh
$ sudo -H pip3 install pipenv   // Install pipenv library
$ cd xxx/flask-skeleton         // Go to the flask-skeleton folder
$ pipenv install                // Create virtual environment and install all packages
$ pipenv shell                  // Activate virtual environment
$ export FLASK_APP=flasky.py    // Set environmnt variable
$ flask run                     // Run flask server
```

### Change config settings

```sh
$ export APP_SETTINGS="project.server.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.server.config.ProductionConfig"
```

### Create DB

```sh
$ flask create_db
$ flask db init
$ flask db migrate
$ flask create_admin
$ flask create_data
```

### Run the Application

```sh
$ flask run
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

### Testing

Without coverage:

```sh
$ flask test
```

With coverage:

```sh
$ flask cov
```
