from flask import g, current_app
import pymongo


def get_db() -> pymongo.collection.Collection:
    mongo_db = current_app.config['MONGO_DATABASE']
    mongo_username = current_app.config.get('MONGO_USERNAME')
    mongo_pwd = current_app.config.get('MONGO_PASSWORD')

    db = getattr(g, 'db', None)

    if db is None:
        mongo_uri = current_app.config['MONGO_URI']

        db = pymongo.MongoClient(mongo_uri,
                                 username=mongo_username,
                                 password=mongo_pwd)
        g.db = db

    return db[mongo_db]


def init_db() -> None:
    db = get_db()
    db.patient_documents.create_index('digest_code',
                                      name='digest_code_idx',
                                      unique=True,
                                      background=True)
