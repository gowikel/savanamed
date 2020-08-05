from ..interfaces.database import DatabaseInterface
from ..interfaces.text import TextInterface
from savanamed.db import get_db

import pymongo


class MongoDatabaseAdapter(DatabaseInterface):
    """
    This is a connector between the database and PatientReport
    """

    @staticmethod
    def has_been_saved(text: TextInterface) -> bool:
        """
        Checks that the given text has been saved. The text
        must be anonymous
        """
        digest_code = text.digest_code

        return bool(MongoDatabaseAdapter.retrieve_document(digest_code))

    @staticmethod
    def save_document(text: TextInterface) -> None:
        """
        Saves the given document.
        """
        db = get_db()
        digest_code = text.digest_code
        patient_id = text.original_id
        free_text = text.data

        document = {
            'digest_code': digest_code,
            'patient_id': patient_id,
            'free_text': free_text,
        }

        db.patient_documents.insert_one(document)

    @staticmethod
    def save_if_not_has_been_saved(text: TextInterface) -> bool:
        """
        Saves the given document if it has not been saved
        """
        has_text_been_saved = MongoDatabaseAdapter.has_been_saved(text)
        if not has_text_been_saved:
            MongoDatabaseAdapter.save_document(text)
        return not has_text_been_saved

    @staticmethod
    def retrieve_document(document_digest: str) -> pymongo.collection.Cursor:
        """
        Returns the document that contains a given digest
        """
        db = get_db()
        search_params = {
            'digest_code': document_digest,
        }

        return db.patient_documents.find_one(search_params)
