from rdflib import Graph, Namespace, BNode, plugin
from rdflib.namespace import RDF, DC, XSD, FOAF
from rdflib.store import Store

from flask import request, g
from werkzeug.local import LocalProxy

from datapub import app


DCAT = Namespace('http://www.w3.org/ns/dcat#')
catalog_node = BNode('catalog')


def get_site_namespace():
    return Namespace(request.url_root)


def get_graph():
    graph = getattr(g, '_graph', None)
    if graph is None:
        graph = g._graph = _get_graph()
    return graph


def _get_graph():
    cat_ident = app.config['CATALOG_ID']
    cat_db = app.config['DATABASE_URI']
    cat_store = plugin.get('SQLAlchemy', Store)(identifier=cat_ident)
    graph = Graph(cat_store, identifier=cat_ident)
    graph.open(cat_db, create=True)
    prepare_graph(graph)
    return graph


def prepare_graph(graph):
    ## Bind standard namespaces
    ##----------------------------------------
    ## note: we need to bind **only once**!
    ## it looks like they get rebound anyways each time we reload the server..
    graph.bind('dc', DC, override=True)
    graph.bind('xsd', XSD, override=True)
    graph.bind('foaf', FOAF, override=True)
    graph.bind('dcat', DCAT, override=True)

    ## Make sure we have the catalog entry
    ##----------------------------------------
    graph.set((catalog_node, RDF.type, DCAT.Catalog))


@app.teardown_appcontext
def teardown_graph(exception):
    ## todo: here we can disconnect the sqlalchemy connection, ...
    pass

graph = LocalProxy(get_graph)
