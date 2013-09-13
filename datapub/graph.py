from rdflib import Graph, Namespace, BNode, plugin
from rdflib.namespace import RDF, DC, XSD, FOAF
from rdflib.store import Store

from datapub import app


## Prepare the RDF graph
##----------------------------------------
DCAT = Namespace('http://www.w3.org/ns/dcat#')
cat_ident = app.config['CATALOG_ID']
cat_db = app.config['DATABASE_URI']
cat_store = plugin.get('SQLAlchemy', Store)(identifier=cat_ident)
graph = Graph(cat_store, identifier=cat_ident)
graph.open(cat_db, create=True)

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
catalog = BNode('catalog')
cat_description = (catalog, RDF.type, DCAT.Catalog)
graph.set(cat_description)
