# DataPub

[![Build Status](https://travis-ci.org/rshk/datapub.png)](https://travis-ci.org/rshk/datapub)

Simple data publishing application.

## Abstract

DataPub is a simple application allowing publication (upload)
of datasets in different formats.

Features offered are:

* Administration UI to upload and manage datasets + resources
* A RESTful API offering access to the published data
* (Optionally) a Web UI to display the published data, including
  (pluggable) visualizations of the data.

Then, of course, it should be as easy as possible to extend
the application to provide extra functionality, etc.


## Technologies

* Python
* Flask, as the web framework
* SQLAlchemy, to provide database abstraction

Recommended database: PostgreSQL

It may be worth adding ElasticSearch for nicer searches too,
but that should go in a separate app / plugin, imho.
