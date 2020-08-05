from ..interfaces.text import TextInterface
from hashlib import sha3_512

import re


class TextAdapter(TextInterface):

    header_regex = [
        ('PATIENT_NAME', r'[^RE:]*RE:[ \t]*(?P<PATIENT_NAME_VALUE>.*)'),

        ('RECEPTION_DATE',
         r'[^DATE:]*DATE:[ \t]*(?P<RECEPTION_DATE_VALUE>.*)'),

        ('BIRTH', r'[^DOB:]*DOB:[ \t]*(?P<BIRTH_VALUE>.*)'),
        ('MR', r'[^MR:]*MR:[ \t]*(?P<MR_VALUE>.*)')
    ]

    tok_regex = '|'.join(
        f'(?P<{name}>{regex})' for name, regex in header_regex
    )

    footer_regex = r'([A-Z][A-Za-z]+ ?)+, (\w\.)+'

    def __init__(self, data: str = None):
        if data is None:
            data = ''

        self._digest_code = None
        self._original_id = None

        super().__init__(data)

    def anonymize(self) -> None:
        """
        Removes patient data and returns a hash that represents
        the removed data
        """
        if self._digest_code:
            return

        m = sha3_512()

        patient_data = {}

        for mo in re.finditer(self.tok_regex, self.data):
            kind = mo.lastgroup
            value_key = f'{kind}_VALUE'
            value = mo.groupdict()[value_key]

            patient_data[kind] = value

        for key, value in sorted(patient_data.items()):
            normalized_data = f'{key}: {value}'
            normalized_binary = normalized_data.encode('utf-8')
            m.update(normalized_binary)

            if key == 'MR':
                self._original_id = value

        self.data = re.sub(self.tok_regex, '', self.data).strip()
        self._digest_code = m.hexdigest()

    @property
    def digest_code(self) -> str:
        """
        Returns a digest code that represents anonymized data. If the
        data has not been anonymized, it raises a RuntimeException
        """
        if self._digest_code:
            return self._digest_code

        raise RuntimeError('Text has not been anonymized')

    @property
    def original_id(self) -> str:
        """
        Returns the original patient ID before the anonymization started
        """
        if self._original_id:
            return self._original_id

        raise RuntimeError('Text has not been anonymized')
