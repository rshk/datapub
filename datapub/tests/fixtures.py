"""
Test fixtures
"""

import os
import tempfile

import pytest


__all__ = ['app']


@pytest.fixture
def app(request):
    from datapub import app
    from datapub.models import db

    with app.app_context():
        temp_fd, temp_filename = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + temp_filename
        # todo: we need to run tests against PostgreSQL too
        # maybe, read the DB URI from an env var?
        app.config['TESTING'] = True
        db.create_all()

        def cleanup():
            os.close(temp_fd)
            os.unlink(temp_filename)

        request.addfinalizer(cleanup)
        return app.test_client()
