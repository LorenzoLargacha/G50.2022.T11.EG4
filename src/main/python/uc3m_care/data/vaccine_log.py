""" Module """
from datetime import datetime
from uc3m_care.parser.attribute_date_signature import DateSignature


class VaccineLog:
    def __init__(self, date_signature) -> None:
        self.__date_signature = DateSignature(date_signature).value
        self.__date = datetime.utcnow().__str__()

    @property
    def date_signature(self):
        return self.__date_signature
