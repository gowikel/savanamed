from savanamed.pdf2text.adapters.pdfconverter import PDFConverterAdapter

import pytest


@pytest.mark.parametrize(
    "data", [None, 'invalid pdf', b'invalid pdf', 12]
)
def test_can_be_initialized_with_anything(data):
    pdf = PDFConverterAdapter(data)
    if data is None:
        assert pdf.data is None
    else:
        assert pdf.data == data


@pytest.mark.parametrize(
    "data", [None, 'invalid pdf', b'invalid pdf', 12]
)
def test_no_pdf_data_marks_the_pdf_as_invalid(data):
    pdf = PDFConverterAdapter(data)
    assert not pdf.is_valid()


@pytest.mark.parametrize(
    "data", [None, 12]
)
def test_no_text_data_marks_the_mimetype_as_none(data):
    pdf = PDFConverterAdapter(data)
    assert pdf.mimetype is None


def test_when_initialized_with_none_no_data_error_is_set():
    pdf = PDFConverterAdapter(None)
    assert not pdf.is_valid()
    assert pdf.error == 'There is no data'


def test_when_initialized_with_invalid_mimetypes_error_is_set():
    pdf = PDFConverterAdapter(b'plain text here')
    assert not pdf.is_valid()
    assert pdf.mimetype == 'text/plain'
    assert pdf.error == 'Invalid mimetype: text/plain'


def test_valid_pdf_binary_initalizes_mimetype_to_application_pdf(pdfdata):
    pdf = PDFConverterAdapter(pdfdata)
    assert pdf.mimetype == 'application/pdf'


def test_valid_pdf_binary_marks_the_adapter_as_valid(pdfdata):
    pdf = PDFConverterAdapter(pdfdata)
    assert pdf.is_valid()


def test_valid_pdf_binary_marks_the_error_as_none(pdfdata):
    pdf = PDFConverterAdapter(pdfdata)
    assert pdf.error is None


def test_invalid_binary_renders_empty_text():
    pdf = PDFConverterAdapter(b'I am plain text')
    assert pdf.to_text() == ''


def test_valid_binary_renders_pdf_text(pdfdata):
    pdf = PDFConverterAdapter(pdfdata)

    pdftext = pdf.to_text()

    assert 'DIAGNOSES:' in pdftext
    assert '3. Recurrent transient ischemic attacks.' in pdftext
    assert 'HISTORY OF PRESENT ILLNESS:' in pdftext
    assert ('This is a 59-year-old, right-handed woman with a '
            'history of hypertension, schizophrenia, and') in pdftext
