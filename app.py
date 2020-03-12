#!/usr/bin/env python3

import logging
import logmatic
import os
import sys

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from requestid import requestid, RequestIdFilter


log_level = getattr(logging, os.environ.get('APP_LOG_LEVEL', 'INFO'))
# Configure JSON filesystem log handler
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logmatic.JsonFormatter())
handler.addFilter(RequestIdFilter())
# Configure global logger
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(log_level)
# Create app and database session
app = Flask('flask-demo-app')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('APP_DATABASE_URI')
db = SQLAlchemy(app)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), unique=False)
    comment = db.Column(db.String(120), unique=False)

    def as_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'comment': self.comment
        }


@app.before_first_request
def setup():
    # Configure application logger
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)
    # Bootstrapping database schema
    db.create_all()


@requestid
@app.route('/api/v1/entries', methods=['GET'])
def list_entries():
    entries = list(map(lambda x: x.as_dict(), Entry.query.all()))
    app.logger.info('Retrieved %d entries' % len(entries))
    return make_response(jsonify(entries), 200)


@requestid
@app.route('/api/v1/entries/<id>', methods=['GET'])
def list_entry(id):
    entry = Entry.query.get(id)
    if entry:
        app.logger.info('Entry found for id %s: %s' % (id, entry.as_dict()))
        return make_response(jsonify(entry.as_dict()), 200)
    else:
        app.logger.info('Entry not found for id %s' % id)
        return make_response(jsonify(''), 404)


@requestid
@app.route('/api/v1/entries', methods=['POST'])
def add_entry():
    content = request.json
    entry = Entry()
    entry.description = content['description']
    entry.comment = content['comment']
    db.session.add(entry)
    db.session.commit()
    app.logger.info('Added entry: %s' % entry.as_dict())
    return make_response(jsonify(entry.as_dict()), 200)


@requestid
@app.route('/api/v1/entries/<id>', methods=['POST'])
def update_entry(id):
    content = request.json
    content.pop('id', None)
    db.session.query(Entry).filter_by(id=id).update(content)
    entry = Entry.query.get(id)
    if entry:
        db.session.commit()
        app.logger.info('Updated entry %s with data: %s' % (id, content))
        return make_response(jsonify(entry.as_dict()), 200)
    else:
        app.logger.info('Entry not found for id %s' % id)
        return make_response(jsonify(''), 404)


@requestid
@app.route('/api/v1/entries/<id>', methods=['DELETE'])
def remove_entry(id):
    entry = Entry.query.get(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        app.logger.info('Removed entry: %s', entry.as_dict())
        return make_response(jsonify(entry.as_dict()), 200)
    else:
        app.logger.info('Entry not found for id %s' % id)
        return make_response(jsonify(''), 404)


@app.route('/api/v1/status', methods=['GET'])
def status():
    return make_response(jsonify('OK'), 200)


@requestid
@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return make_response(jsonify(exception), 500)


if __name__ == "__main__":
    host = os.environ.get('APP_HOST', '0.0.0.0')
    port = os.environ.get('APP_PORT', 5000)
    app.run(host=host, port=port)
