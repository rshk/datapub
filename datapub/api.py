"""
The DataPub API

GET /

    301 -> /catalog

GET /catalog[.format]

    Get metadata information about the catalog.

GET /catalog/<dataset>[.format]

    Get metadata information about a dataset.

"""

import json

import flask
from flask import request
from rdflib import Graph

from .app import app
from .graph import graph


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
