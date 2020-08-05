from io import BytesIO


def test_post_without_data_returns_an_error(client):
    response = client.post('/api/v1/pdf2text/')
    status_code = response.status_code
    json = response.json

    assert status_code == 200
    assert 'msg' in json.keys()
    assert 'converted_data' in json.keys()
    assert json['msg'] == 'There is no data'
    assert json['converted_data'] == ''


def test_post_with_pdf_data_returns_text(client, pdffile):
    data = {
        'data': (pdffile, 'data.pdf'),
    }
    response = client.post('/api/v1/pdf2text/',
                           content_type='multipart/form-data',
                           data=data)
    status_code = response.status_code
    json = response.json

    assert status_code == 200
    assert 'msg' in json.keys()
    assert 'converted_data' in json.keys()
    assert json['msg'] == 'OK'
    assert ('This is a 59-year-old, right-handed woman '
            'with a history of hypertension, '
            'schizophrenia, and a') in json['converted_data']


def test_post_checks_detects_pdfs_with_wrong_extension(client, pdffile):
    data = {
        'data': (pdffile, 'data.gif'),
    }
    response = client.post('/api/v1/pdf2text/',
                           content_type='multipart/form-data',
                           data=data)
    status_code = response.status_code
    json = response.json

    assert status_code == 200
    assert 'msg' in json.keys()
    assert 'converted_data' in json.keys()
    assert json['msg'] == 'OK'
    assert ('This is a 59-year-old, right-handed woman '
            'with a history of hypertension, '
            'schizophrenia, and a') in json['converted_data']


def test_post_returns_empty_with_no_pdf_files(client):
    plain_text_file = BytesIO(b'Umm, no PDF here.')
    data = {
        'data': (plain_text_file, 'data.txt'),
    }
    response = client.post('/api/v1/pdf2text/',
                           content_type='multipart/form-data',
                           data=data)
    status_code = response.status_code
    json = response.json

    assert status_code == 200
    assert 'msg' in json.keys()
    assert 'converted_data' in json.keys()
    assert json['msg'] == 'Invalid mimetype: text/plain'
    assert json['converted_data'] == ''


def test_post_returns_an_anonymized_test(client, pdffile):
    data = {
        'data': (pdffile, 'data.gif'),
    }
    response = client.post('/api/v1/pdf2text/',
                           content_type='multipart/form-data',
                           data=data)
    status_code = response.status_code
    json = response.json

    assert status_code == 200
    assert 'msg' in json.keys()
    assert 'converted_data' in json.keys()
    assert json['msg'] == 'OK'

    assert 'MD:' not in json['converted_data']
    assert 'Debra Jones' not in json['converted_data']
    assert 'DATE:' not in json['converted_data']
    assert '12/01/10' not in json['converted_data']
    assert 'RE:' not in json['converted_data']
    assert 'DOB:' not in json['converted_data']
    assert '12/01/65' not in json['converted_data']


def test_document_is_stored_on_db(client, db, pdffile):
    data = {
        'data': (pdffile, 'data.pdf'),
    }
    client.post('/api/v1/pdf2text/',
                content_type='multipart/form-data',
                data=data)
    assert db.patient_documents.count_documents({}) == 1


def test_a_repeated_document_is_only_stored_once(client, db, pdffile):
    pdfdata = pdffile.read()
    data = {
        'data': (BytesIO(pdfdata), 'data.pdf'),
    }
    client.post('/api/v1/pdf2text/',
                content_type='multipart/form-data',
                data=data)

    data = {
        'data': (BytesIO(pdfdata), 'data.pdf'),
    }
    client.post('/api/v1/pdf2text/',
                content_type='multipart/form-data',
                data=data)

    assert db.patient_documents.count_documents({}) == 1


def test_msg_informs_when_a_repeated_document_is_set(client, pdffile):
    pdfdata = pdffile.read()
    data = {
        'data': (BytesIO(pdfdata), 'data.pdf'),
    }
    client.post('/api/v1/pdf2text/',
                content_type='multipart/form-data',
                data=data)

    data = {
        'data': (BytesIO(pdfdata), 'data.pdf'),
    }
    response = client.post('/api/v1/pdf2text/',
                           content_type='multipart/form-data',
                           data=data)
    status_code = response.status_code
    json = response.json

    assert status_code == 200
    assert 'msg' in json.keys()
    assert json['msg'] == ('OK. The document was already stored '
                           'in the database')


def test_converted_data_is_returned_filled_with_duplicated_documents(client,
                                                                     pdffile):
    pdfdata = pdffile.read()
    data = {
        'data': (BytesIO(pdfdata), 'data.pdf'),
    }
    client.post('/api/v1/pdf2text/',
                content_type='multipart/form-data',
                data=data)

    data = {
        'data': (BytesIO(pdfdata), 'data.pdf'),
    }
    response = client.post('/api/v1/pdf2text/',
                           content_type='multipart/form-data',
                           data=data)
    status_code = response.status_code
    json = response.json

    assert status_code == 200
    assert 'converted_data' in json.keys()
    assert ('This is a 59-year-old, right-handed woman '
            'with a history of hypertension, '
            'schizophrenia, and a') in json['converted_data']
