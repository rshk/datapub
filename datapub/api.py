"""
The DataPub API

GET /

    301 -> /catalog

GET /catalog[.format]

    Get metadata information about the catalog.

GET /catalog/<dataset>[.format]

    Get metadata information about a dataset.

"""

import hashlib
import json
import re
import os

import flask
from flask import request
from rdflib import Graph

from .app import app
from .graph import graph


RE_SHA1 = re.compile(r'^[0-9a-fA-F]{40}$')


SERIALIZATION_FORMATS = {
    # Extension, description, mimetype, serializer
    'rdf': ('RDF+XML format', 'application/rdf+xml', 'pretty-xml'),
    'n3': ('n3 serialized RDF', 'text/rdf+n3', 'n3'),
    'nquads': ('nquads serialized RDF', 'text/plain', 'nquads'),
    'nt': ('nt serialized RDF', 'text/plain', 'nt'),
    # 'trig': ('trig serialized RDF', 'text/plain', 'trig'),
    # 'trix': ('trix serialized RDF', 'text/plain', 'trix'),
    'turtle': ('turtle serialized RDF', 'application/x-turtle', 'turtle'),
}


def load_graph_from_request(request):
    g = Graph()
    g.parse(data=request.data, format='n3')
    return g


@app.route('/')
def homepage():
    return flask.redirect(flask.url_for('catalog_view'))


@app.route('/catalog', methods=['GET', 'POST', 'DELETE'])
@app.route('/catalog.<fmt>')
def catalog_view(fmt=None):
    global graph

    if request.method == 'GET':
        ## GET is used to get catalog information
        ## todo: we should apply filters here, we do not want to return
        ##       the whole graph at once!
        if fmt is None:
            ## If no format specified, return a list of choices
            choices = dict(('/catalog.{}'.format(k), v[0])
                           for k, v in SERIALIZATION_FORMATS.iteritems())
            return (json.dumps(choices, indent=4),
                    300, {'Content-Type': 'application/json'})

        ## Return the serialized graph
        fmtdef = SERIALIZATION_FORMATS[fmt]
        return (graph.serialize(format=fmtdef[2]),
                200, {'Content-Type': fmtdef[1]})

    elif request.method == 'POST':
        ## POST is used to add triples
        g2 = load_graph_from_request(request)
        for triple in g2:
            graph.add(triple)
        return json.dumps({'message': "{} triples inserted".format(len(g2))})

    elif request.method == 'PATCH':
        ## POST is used to set values
        g2 = load_graph_from_request(request)
        for triple in g2:
            graph.set(triple)
        return json.dumps({'message': "{} triples updated".format(len(g2))})

    elif request.method == 'DELETE':
        ## DELETE is used to delete triples
        g2 = load_graph_from_request(request)
        for triple in g2:
            graph.delete(g2)
        return json.dumps({'message': "{} triples deleted".format(len(g2))})


@app.route('/blobs', methods=['GET', 'POST'])
def blobs_view(blob_id=None):
    """
    Blobs storage API. Allows GET|POST|DELETE of binary files.

    POST /blobs

        Allows uploading a file; the file will be stored by its sha1 sum

    GET /blobs/<sha1>

        Returns the content of the blob itself

    DELETE /blobs/<sha1>

        Deletes the specified blob
    """
    if request.method == 'POST':
        if blob_id is not None:
            return "You cannot POST content for a blob by id", 400

        ## Now we need to save the file
        new_file = request.files['file']

        ## Now, we can read the file in chunks to calculate
        ## its sha1 sum
        sha1 = hashlib.sha1()
        while True:
            data = new_file.read(1024**2)
            if not data:
                break
            sha1.update(data)
        sha1 = sha1.hexdigest()

        ## Then, store it
        new_file.seek(0)
        ## todo: we can store files in a smarter way, eg.
        ##       creating some subfolders...
        file_dest = os.path.join(app.config['UPLOAD_FOLDER'], sha1)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        new_file.save(file_dest)

        ## todo: store information about the blob in the graph
        # How do we store it?

        ## </blobs/sha1> <rdf:type>
        ##               <dcat:mediaType> <...>

        return (json.dumps({'blob_id': sha1}), 201,
                {'Content-Type': 'application/json',
                 'Location': flask.url_for('blob_view', blob_id=sha1)})


@app.route('/blobs/<blob_id>', methods=['GET', 'DELETE'])
def blob_view(blob_id):
    ## Check that the blob id is valid
    if not RE_SHA1.match(blob_id):
        return json.dumps({'message': 'Invalid blob id'}), 400

    ## Build file name; if the file doesn't exist, return 404'
    blob_file = flask.safe_join(app.config['UPLOAD_FOLDER'], blob_id)
    if not os.path.exists(blob_file):
        return json.dumps({'message': 'File not found'}), 404

    if request.method == 'GET':
        ## Return the content of the file

        ## todo: it would be nice to return the correct mimetype of the file
        ## (guessed using python-magic?) and its original file name;
        ## maybe we can store them in the triple store..?

        ## note: the user-specified filename and mimetype must be attached
        ## to the distribution, **not** the blob, as blobs can possibly
        ## be attached to multiple distributions.

        return flask.send_file(blob_file,
                               mimetype='application/octet-stream',
                               as_attachment=True)

    elif request.method == 'DELETE':
        ## todo: be careful here, as we want to check that the blob
        ## is not referenced in the graph..

        os.unlink(blob_file)
        return json.dumps({'message': 'Blob {0} deleted'.format(blob_id)})

    assert False, "Something went wrong (disallowed method passed through)"
