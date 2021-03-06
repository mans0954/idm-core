# IdM Core API

[![Build Status](https://travis-ci.org/alexsdutton/idm-core.svg?branch=master)](https://travis-ci.org/alexsdutton/idm-core) [![codecov](https://codecov.io/gh/alexsdutton/idm-core/branch/master/graph/badge.svg)](https://codecov.io/gh/alexsdutton/idm-core)

A prototypical identity API supporting:

* Names (and not just first/last)
* Nationalities
* Affiliations and roles
* Sex
* Source documents, and the personal information they attest
* Publishing data changes to AMQP


## Getting started

Make rabbitmq available on localhost with a `guest:guest` administrator account.

    mkvirtualenv idm-core --python=/usr/bin/python3
    pip install -r requirements.txt

    createdb idm_core
    django-admin.py migrate

    # Set a celery worker going
    celery -B -A idm_core worker -l info &

    # Run the dev server
    django-admin.py runserver

    # Create a new person
    curl http://localhost:8000/person/ -d@examples/lewis-carroll.json -H"Content-type: application/json" -v


## Architecture

The IdM Core component is designed to support a collaborative approach to identity management.


### Model mixins:

* Attestable
* Manageable
* Suspendable (not yet implemented)
