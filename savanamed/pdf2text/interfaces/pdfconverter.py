from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from ..interfaces.text import TextInterface


class PDFConverterInterface(ABC):
    """
    PDFConverterInterface represents a common interface to
    all the operations related with the conversion of PDF files
    to text.
    """

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Checks if a passed PDF is valid or not
        :return: True if the PDF is valid, False otherwise
        """
        pass

    @abstractmethod
    def to_text(self) -> TextInterface:
        """
        Converts the given PDF into text. If the PDF is
        not valid it just return an empty string
        :return: A string that represents the PDF
        """
        pass

    @property # type: ignore
    @abstractmethod
    def error(self) -> str:
        """
        Returns a descriptive string of why the given PDF is not valid
        """
        pass

    @error.setter # type: ignore
    @abstractmethod
    def error(self, value: str) -> None:
        """
        Allows to change the error description
        """
        pass

    @staticmethod
    @abstractmethod
    def get_from_request() -> PDFConverterInterface:
        """
        Helper function that wraps the Flask requests contents with
        the given adapter. It should look for a given file from the
        HTTP protocol and wrap it into the adapter.
        """
        pass

    @property
    @abstractmethod
    def data(self) -> Any:
        """
        Returns the PDF data
        """
        pass
