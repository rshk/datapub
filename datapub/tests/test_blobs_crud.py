"""
Tests for the DataPub blobs CRUD
"""
import hashlib
import json
import textwrap
from io import BytesIO

from .fixtures import app


def test_file_upload(app):
    payload = textwrap.dedent("""
    Hello, world!
    This is just an example text file.
    This is the content of the example text file.
    """)
    payload_sha1 = hashlib.sha1(payload).hexdigest()

    resp = app.post('/blobs', data={
        'file': (BytesIO(payload), 'hello.txt', 'text/plain')
    })

    ## Status code must be 201 Created
    assert resp.status_code == 201

    ## test the Location: header content
    new_loc = resp.headers['Location']
    assert payload_sha1 in new_loc
    assert new_loc.endswith('/blobs/{0}'.format(payload_sha1))

    ## Test the blob_id parameter in the response json
    resp_data = json.loads(resp.data)
    assert resp_data['blob_id'] == payload_sha1

    ## Check object returned by requesting the url in the Location header
    resp = app.get(new_loc)
    assert resp.status_code == 200
    assert resp.data == payload

    ## Delete the blob and check it was removed correctly
    resp = app.delete(new_loc)
    assert resp.status_code == 200

    ## Make sure we get a 404 meaning the file was deleted correctly
    resp = app.get(new_loc)
    assert resp.status_code == 404
