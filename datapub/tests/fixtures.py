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

    with app.app_context():
        temp_fd, temp_filename = tempfile.mkstemp()
        app.config['DATABASE_URI'] = 'sqlite:///' + temp_filename
        app.config['TESTING'] = True
        #db.create_all()

        def cleanup():
            os.close(temp_fd)
            os.unlink(temp_filename)

        request.addfinalizer(cleanup)
        return app.test_client()
