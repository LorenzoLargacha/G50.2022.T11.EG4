""" Module """
from datetime import datetime


class VaccineLog():
    def __init__(self, date_signature: str) -> None:
        self.__date_signature = date_signature
        self.__date = datetime.utcnow().__str__()
