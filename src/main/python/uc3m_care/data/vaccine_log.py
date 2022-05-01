""" Module """
from datetime import datetime
from uc3m_care.data.attribute.attribute_date_signature import DateSignature


class VaccineLog:
    def __init__(self, date_signature) -> None:
        self.__date_signature = DateSignature(date_signature).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)

    @property
    def date_signature(self):
        return self.__date_signature

    @date_signature.setter
    def date_signature(self, value):
        self.__date_signature = DateSignature(value).value

    @property
    def time_stamp (self):
        return self.__timestamp

    @time_stamp.setter
    def time_stamp (self, value):
        self.__time_stamp = value

