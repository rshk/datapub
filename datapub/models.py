"""
DataPub database models
"""

#from datacat import db

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # then: db.init_app(app)


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    dataset = db.relationship(
        'Dataset', backref=db.backref('resources', lazy='dynamic'))
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    # todo: add a column for the blob itself
    #       then, we'll store it outside and just keep
    #       a reference here
    content_type = db.Column(db.String(128))
    file_name = db.Column(db.String(128))  # original file name
