from flask.testing import FlaskClient
from importlib.resources import read_binary
from io import BytesIO
from savanamed import create_app
from typing import IO
from tests import faker
from random import shuffle

import pytest
import inject
import os
import pymongo


@pytest.fixture(scope='function')
def db() -> pymongo.collection.Collection:
    mongo_db = os.environ.get('MONGO_DATABASE', 'savanamed_test')
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    mongo_username = os.environ.get('MONGO_USERNAME')
    mongo_pwd = os.environ.get('MONGO_PASSWORD')

    print(f'{mongo_username}:{mongo_pwd}')

    os.environ['MONGO_DATABASE'] = mongo_db
    os.environ['MONGO_URI'] = mongo_uri

    connection = pymongo.MongoClient(mongo_uri,
                                     username=mongo_username,
                                     password=mongo_pwd)
    db = connection[mongo_db]
    yield db
    connection.drop_database(mongo_db)


@pytest.fixture
def client(db) -> FlaskClient:
    inject.clear()

    os.environ['FLASK_ENV'] = 'testing'

    application = create_app()
    application.testing = True
    return application.test_client()


@pytest.fixture()
def pdfdata() -> bytes:
    package = 'tests.resouces'
    resouce = 'Report1.pdf'
    return read_binary(package, resouce)



@pytest.fixture()
def pdffile(pdfdata) -> IO:
    return BytesIO(pdfdata)


@pytest.fixture()
def patient_report_header():
    """
    Generates Fake patient data and returns a dictionary with
    all given data and a string that contains all the information
    :return:
    """
    def wrapper(ordered=True, header=None):
        date_fmt = '%d/%m/%Y'

        if header is None:
            patient_name = faker.name()
            patient_birth = faker.date_of_birth()
            patient_birth_str = patient_birth.strftime(date_fmt)
            patient_mr = faker.ssn()
            patient_record_date = faker.date_between(start_date=patient_birth)
            patient_record_date_str = patient_record_date.strftime(date_fmt)

            patient_data = {
                'RE': patient_name,
                'DATE': patient_record_date_str,
                'MR': patient_mr,
                'DOB': patient_birth_str,
            }
        else:
            patient_data = header

        patient_data_keys = sorted(patient_data.keys())

        if not ordered:
            shuffle(patient_data_keys)

        patient_values = []
        for key in patient_data_keys:
            patient_values.append(f'{key}: {patient_data[key]}')

        header_str = '\n'.join(patient_values)

        return patient_data, header_str
    return wrapper


@pytest.fixture()
def patient_report(patient_report_header):
    """
    This fixture returns three things upon invocation:

    - Random generated patient data
    - A free text
    - A text that combines all those things

    The ordered flag can be used to sort patient data in the final
    text or to shuffle it.

    The header flag can be used to create a new patient report with the same
    header data.
    """
    def wrapper(ordered=True, header=None):
        date_fmt = '%d/%m/%Y'

        patient_data, header_str = patient_report_header(ordered=ordered,
                                                         header=header)

        free_text = faker.text()

        final_text = f'{header_str}\n\n{free_text}'
        return patient_data, free_text, final_text

    return wrapper
