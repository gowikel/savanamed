from savanamed.pdf2text.adapters.text import TextAdapter
from collections import UserString

import pytest


def test_text_adapter_is_a_modified_string():
    text = TextAdapter('lololo')
    assert isinstance(text, UserString)


def test_text_adapter_can_be_initialized_with_none():
    text = TextAdapter()
    assert text.data == ''


def test_text_adapter_can_return_strings():
    text = TextAdapter('my nice and beautiful string')

    assert text.data == 'my nice and beautiful string'
    assert text.to_unicode() == 'my nice and beautiful string'


def test_text_adapter_can_anonymize_data(patient_report):
    header, free_text, final_text = patient_report()
    text = TextAdapter(final_text)
    text.anonymize()

    for key in header.keys():
        assert key not in text.data


def test_text_cannot_access_digest_code_property_without_anonymize_call():
    text = TextAdapter('some random data here')
    with pytest.raises(RuntimeError, match=r'Text has not been anonymized'):
        text.digest_code


def test_digest_code_is_initialized_after_anonymize_call():
    text = TextAdapter('some random data')
    text.anonymize()

    assert text.digest_code


def test_digest_code_only_depends_on_patient_data():
    text1 = TextAdapter('no patient data')
    text2 = TextAdapter('but I do not have patient data either')

    text1.anonymize()
    text2.anonymize()

    assert text1.digest_code == text2.digest_code


def test_two_equal_patients_have_the_same_digest_code(patient_report):
    header, free_text, final_text = patient_report()
    header2, free_text2, final_text2 = patient_report(header=header)

    text1 = TextAdapter(final_text)
    text2 = TextAdapter(final_text2)

    text1.anonymize()
    text2.anonymize()

    assert text1.digest_code == text2.digest_code


def test_different_headers_create_different_digest_codes(patient_report):
    header, free_text, final_text = patient_report()
    header2, free_text2, final_text2 = patient_report()

    text1 = TextAdapter(final_text)
    text2 = TextAdapter(final_text2)

    text1.anonymize()
    text2.anonymize()

    assert text1.digest_code != text2.digest_code


def test_patient_data_order_is_irrelevant_on_digest_codes(patient_report):
    header, free_text, final_text = patient_report()
    header2, free_text2, final_text2 = patient_report(header=header,
                                                      ordered=False)

    text1 = TextAdapter(final_text)
    text2 = TextAdapter(final_text2)

    text1.anonymize()
    text2.anonymize()

    assert text1.digest_code == text2.digest_code


def test_anonymize_keeps_free_text_untouched(patient_report):
    header, free_text, final_text = patient_report()

    text = TextAdapter(final_text)
    text.anonymize()

    assert free_text in text.data


def test_original_id_property_is_set_after_a_call_to_anonymize(patient_report):
    header, free_text, final_text = patient_report()

    text = TextAdapter(final_text)
    text.anonymize()

    assert text.original_id


def test_original_id_cannot_be_accesed_without_anonymize_call(patient_report):
    header, free_text, final_text = patient_report()

    text = TextAdapter(final_text)

    with pytest.raises(RuntimeError, match=r'Text has not been anonymized'):
        text.original_id


def test_multiple_calls_to_anonymize_do_not_change_data(patient_report):
    header, free_text, final_text = patient_report()

    text = TextAdapter(final_text)

    text.anonymize()

    previous_anonymous_data = text.data
    previous_digest_code = text.digest_code
    previous_original_id = text.original_id

    text.anonymize()

    assert text.data == previous_anonymous_data
    assert text.digest_code == previous_digest_code
    assert text.original_id == previous_original_id
