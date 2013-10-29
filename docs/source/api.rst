API Documentation
#################

Access to the data is exposed through a RESTful API.

.. note::
    Right now, there is **no** authentication in place,
    thus the application should only be used in private environments
    or for testing. User authentication support is a planned feature,
    anyways..


Dataset CRUD
============

List datasets
-------------

``GET /dataset``

Returns a list of datasets.

Supports :ref:`api-pagination` and :ref:`api-fields`.

.. note::
    We need to add some ways to filter datasets (or just a separate
    endpoint for search..?)


Get dataset
-----------

``GET /dataset/<id>``

Returns information about a specific dataset.

Supports :ref:`api-fields`.


Create new dataset
------------------

``POST /dataset``

Accepts a json object.


Update dataset
--------------

``PUT /dataset/<id>``

Accepts a json object, with values to be updated.


Delete dataset
--------------

``DELETE /dataset/<id>``


List dataset resources
----------------------

``GET /dataset/<id>/resources``

Returns a list of resources associated to the dataset.

Supports :ref:`api-pagination` and :ref:`api-fields`.


Resources CRUD
==============

Get resource
------------

``GET /resource/<id>``

Returns the specified resource.

Supports :ref:`api-fields`.


Create resource
---------------

``POST /dataset/<id>/resources``

Accepts a json object.


Update resource
---------------

``PUT /resource/<id>``

Accepts a json object, with values to be updated.


Delete resource
---------------

``DELETE /resource/<id>``

.. note:: this will delete both resource metadata and data.


Get resource content
--------------------

``GET /resource/<id>/content``

Returns the actual resource data. The file will be returned
as-is, with ``Content-disposition: attachment``, its original file name
and ``Content-type``.


Update resource content
-----------------------

``PUT /resource/<id>/content``

The request body will be stored as the resource data; the ``Content-type``
request header will be used as the stored content type.

.. note:: How to set the file name from the request? Custom header..?



.. _api-pagination:

Pagination
==========

Pagination is so handled in views:

* The ``page`` argument controls the page number, starting from ``0``.
* The ``per_page`` argument controls the maximum amount of items per page.
* The ``Link:`` response header contains links to the ``first``, ``prev``,
  ``next``, ``last`` pages.

.. note::
    We might also want to return the total number of results too,
    in the response headers.


.. _api-fields:

Controlling returned fields
===========================

The ``fields`` argument may be used to control which fields to
return. Accepted values are:

* A comma-separated list of field names
* ``minimal`` (default): returns very few fields, usually
  ``id`` and ``title``.
* ``all``: returns **all** the fields

.. note:: The ``id`` field is **always** returned.
