from flask import Blueprint, jsonify
from .interfaces.pdfconverter import PDFConverterInterface
from .interfaces.database import DatabaseInterface

import inject


@inject.autoparams()
def create_blueprint(PDF: PDFConverterInterface,
                     DB: DatabaseInterface) -> Blueprint:
    bp = Blueprint('pdf2text', __name__)

    @bp.route('/', methods=('POST',))
    def convert_to_text() -> str:
        """
        This endpoint fetchs a file called data from the HTTP
        and converts it to text.
        """
        pdf = PDF.get_from_request()

        if pdf.is_valid():
            text = pdf.to_text()
            text.anonymize()
            result = DB.save_if_not_has_been_saved(text)
            msg = 'OK'
            if not result:
                msg = ('OK. The document was already stored '
                       'in the database')

            return jsonify(converted_data=text.data,
                           msg=msg)
        else:
            return jsonify(converted_data='',
                           msg=pdf.error)

    return bp
