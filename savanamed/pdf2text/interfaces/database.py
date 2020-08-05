from abc import ABC, abstractmethod
from ..interfaces.text import TextInterface

from typing import Any


class DatabaseInterface(ABC):
    """
    This is a connector between the database and PatientReport
    """

    @staticmethod
    @abstractmethod
    def has_been_saved(text: TextInterface) -> bool:
        """
        Checks that the given text has been saved. The text
        must be anonymous
        """
        pass

    @staticmethod
    @abstractmethod
    def save_document(text: TextInterface) -> None:
        """
        Saves the given document.
        """
        pass

    @staticmethod
    @abstractmethod
    def save_if_not_has_been_saved(text: TextInterface) -> bool:
        """
        Saves the given document if it has not been saved.

        It returns a boolean indicating if the text has been saved
        or not.
        """
        pass

    @staticmethod
    @abstractmethod
    def retrieve_document(document_digest: str) -> Any:
        """
        Returns the document that contains a given digest
        """
        pass
