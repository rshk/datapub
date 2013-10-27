"""
The API blueprint.

We expose:

* CRUD for datasets::

    GET /dataset  -> list all the datasets
    GET /dataset/<id>  -> get the specific dataset
    POST /dataset  -> create a new dataset
    PUT /dataset/<id>  -> update a dataset
    DELETE /dataset/<id>  -> delete a dataset
    GET /dataset/<id>/resources  -> list all the associated resources

* CRUD for resources

    GET /resource/<id>  -> return a specific resource
    GET /resource/<id>/content  -> return the blob linked to resource
    POST /dataset/<id>/resources  -> create a new resource for the dataset
    PUT /resource/<id>  -> update the resource details
    PUT /resource/<id>/content  -> update the resource content
    DELETE /resource/<id>  -> delete a specific resource

.. note::
    Although the read-only API is public,
    we still need user authentication for writing.
"""

import json

from flask import Blueprint, request

from datapub.models import db, Dataset, Resource


bp = api_blueprint = Blueprint('api', __name__)


def json_response(data, status=200):
    return json.dumps(data), status, {
        'Content-type': 'application/json',
    }


def dump_dataset(obj):
    return {
        'id': obj.id,
        'title': obj.title,
        'description': obj.description,
    }


def load_dataset(obj):
    ds = Dataset()
    if 'id' in obj:
        ds.id = obj['id']
    ds.title = obj.get('title')
    ds.description = obj.get('description')
    return ds


def dump_resource(obj):
    return {
        'id': obj.id,
        'title': obj.title,
        'description': obj.description,
        'content_type': obj.content_type,
        'file_name': obj.file_name,
    }


def load_resource(obj):
    res = Resource()
    if 'id' in obj:
        res.id = obj['id']
    res.title = obj.get('title')
    res.description = obj.get('description')
    res.content_type = obj.get('content_type')
    res.file_name = obj.get('file_name')
    return res


@bp.route('/')
def index():
    return "This is the root of the API endpoint"


@bp.route('/dataset')
def list_datasets():
    # todo: apply paging
    objects = Dataset.query.all()
    # we can .paginate(page, per_page)
    # also, remember to set Link: header
    return json_response([
        dump_dataset(obj) for obj in objects
    ])


@bp.route('/dataset/<dataset_id>')
def get_dataset(dataset_id):
    dataset_id = int(dataset_id)
    dataset = Dataset.query.get_or_404(dataset_id)
    return json_response(dump_dataset(dataset))


@bp.route('/dataset', methods=['POST'])
def create_dataset():
    obj = request.json or {}
    model = load_dataset(obj)
    db.session.add(model)
    db.session.commit()
    return json_response(dump_dataset(model), 201)


@bp.route('/dataset/<dataset_id>', methods=['PUT'])
def update_dataset(dataset_id):
    return json_response({'id': dataset_id}, 201)


@bp.route('/dataset/<dataset_id>', methods=['DELETE'])
def delete_dataset(dataset_id):
    # todo: how to delete a model (w/o retrieving it first)?
    #Dataset.query.filter(int(dataset_id)).delete()
    return json_response({'ok': True})


@bp.route('/dataset/<dataset_id>/resources')
def list_dataset_resources(dataset_id):
    dataset_id = int(dataset_id)
    return json_response({'id': dataset_id})


@bp.route('/resource/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    pass


@bp.route('/dataset/<dataset_id>/resources', methods=['POST'])
def create_resource(dataset_id):
    pass
