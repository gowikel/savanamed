from .interfaces.pdfconverter import PDFConverterInterface
from .adapters.pdfconverter import PDFConverterAdapter

from .interfaces.text import TextInterface
from .adapters.text import TextAdapter

from .interfaces.database import DatabaseInterface
from .adapters.database import MongoDatabaseAdapter

import inject


def inject_configuration(binder: inject.Binder) -> None:
    binder.bind(PDFConverterInterface, PDFConverterAdapter)
    binder.bind(TextInterface, TextAdapter)
    binder.bind(DatabaseInterface, MongoDatabaseAdapter)
