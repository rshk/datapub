"""
Tests for the DataPub blobs CRUD
"""

import binascii
#import datetime
#import json
import os
import textwrap
from io import BytesIO

# from rdflib import Graph, Namespace
# from rdflib.namespace import RDF

from .fixtures import app


def test_file_upload(app):
    # boundary = binascii.hexlify(os.urandom(16))
    # headers = {
    #     'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary),
    # }
    # payload = textwrap.dedent("""
    # --{boundary}
    # Content-Disposition: form-data; name="file"; filename="example.txt"
    # Content-Type: text/plain

    # Hello, world!
    # This is just an example text file.
    # This is the content of the example text file.

    # --{boundary}
    # """.format(boundary=boundary))
    payload = textwrap.dedent("""
    Hello, world!
    This is just an example text file.
    This is the content of the example text file.
    """)
    resp = app.post('/blobs', data={
        'file': (BytesIO(payload), 'hello.txt')
    })
    # resp = app.post('/blobs', data=payload, headers=headers)
    assert resp.status_code == 200

    ## todo: test the Location: header content
    ## todo: test the blob_id parameter in the response json