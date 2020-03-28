import couchdb
import os
import logging

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

logger = logging.getLogger('estropadak')

user = os.getenv('COUCH_USER')
logger.info('User %s', user)

passwd = os.getenv('COUCH_PASS')
host = os.getenv('COUCH_HOST')

couch = couchdb.Server('http://%s:%s@%s' % (user, passwd, host))
db = couch['test']

def getdoc(id):
    try:
        return db[id]
    except couchdb.http.ResourceNotFound:
        raise KeyError(f'Document with {id} not found')

def setdoc(id, doc):
    logging.info(f'Creating/updating doc {id}')
    db[id] = doc