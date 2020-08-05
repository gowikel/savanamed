from abc import ABC, abstractmethod
from collections import UserString


class TextInterface(ABC, UserString):
    """
    Wraps an unicode string and makes some functions on in.
    This class must act as a Proxy, so any valid str method
    must be a valid TextInterface method.

    In addition, it will add some methods to process clinical
    texts
    """

    @abstractmethod
    def anonymize(self) -> None:
        """
        Removes patient data and stores a hash that represents removed
        data. This has can be accessed with .digest_code property
        """
        pass

    @property
    @abstractmethod
    def digest_code(self) -> str:
        """
        Returns a digest code that represents anonymized data. If the
        data has not been anonymized, it raises a RuntimeException
        """
        pass

    @property
    @abstractmethod
    def original_id(self) -> str:
        """
        Returns the original patient ID before the anonymization started
        """
        pass

    def to_unicode(self) -> str:
        """
        Returns the underlining text. This is just a proxy of
        the data property, as this class derives from UserString.
        """
        return self.data
