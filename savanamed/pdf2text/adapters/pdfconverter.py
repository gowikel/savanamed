from __future__ import annotations

from flask import request
from io import BytesIO
from pdftotext import PDF
from ..interfaces.pdfconverter import PDFConverterInterface
from ..interfaces.text import TextInterface
from typing import Any

import magic
import inject


class PDFConverterAdapter(PDFConverterInterface):
    """
    PDFInterface adapter that makes use of the pdftotext library
    """

    @inject.autoparams('text_adapter')
    def __init__(self, pdf_binary: bytes, text_adapter: TextInterface):
        self._pdf = pdf_binary

        if isinstance(pdf_binary, bytes):
            self.mimetype = magic.from_buffer(pdf_binary, mime=True)
        else:
            self.mimetype = None
        self._error = None
        self._text_adapter_klass = text_adapter
        super().__init__()

    def is_valid(self) -> bool:
        """
        Checks if a passed PDF is valid or not
        :return: True if the PDF is valid, False otherwise
        """
        if not self.data:
            self.error = 'There is no data'
            return False

        if self.mimetype != 'application/pdf':
            self.error = f'Invalid mimetype: {self.mimetype}'
            return False

        return True

    def to_text(self) -> TextInterface:
        """
        Converts the given PDF into text. If the PDF is
        not valid it just return an empty string
        :return: A string that represents the PDF
        """
        if self.is_valid():
            buffer = BytesIO(self.data)
            pdf = PDF(buffer)
            return self._text_adapter_klass('\n\n'.join(pdf))

        return self._text_adapter_klass('')

    @property
    def error(self) -> str:
        """
        Returns a descriptive string of why the given PDF is not valid
        """
        return self._error

    @error.setter
    def error(self, value: str) -> None:
        """
        Allows to change the error description
        """
        self._error = value

    @staticmethod
    def get_from_request() -> PDFConverterInterface:
        """
        Helper function that wraps the Flask requests contents with
        the given adapter. It should look for a given file from the
        HTTP protocol and wrap it into the adapter.
        """
        if 'data' not in request.files.keys():
            return PDFConverterAdapter(None)

        return PDFConverterAdapter(request.files['data'].stream.read())

    @property
    def data(self) -> Any:
        """
        Returns the PDF data
        """
        return self._pdf
