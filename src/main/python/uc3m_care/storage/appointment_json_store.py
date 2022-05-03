"""Module appointment_json_store"""
import json

from uc3m_care.storage.json_store import JsonStore
from uc3m_care.data.vaccination_appoinment import VaccinationAppoinment
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH


class AppointmentJsonStore(JsonStore):
    """Clase hija de JsonStore con los atributos para store_date"""

    class __AppointmentJsonStore(JsonStore):
        """Clase privada"""
        _FILE_PATH = JSON_FILES_PATH + "store_date.json"
        _ID_FIELD = "_VaccinationAppoinment__date_signature"

        __ERROR_MESSAGE_INVALID_OBJECT = "Invalid vaccination appointment object"
        __ERROR_MESSAGE_FILE_NOT_FOUND = "Store_date not found"

        def __init__(self):
            pass

        def add_item(self, date: VaccinationAppoinment) -> None:
            """Saves an appoinment into a file"""
            if not isinstance(date, VaccinationAppoinment):
                raise VaccineManagementException(self.__ERROR_MESSAGE_INVALID_OBJECT)
            super().add_item(date)

        def find_date_signature(self, date_signature: str) -> VaccinationAppoinment:
            """Checks if a date_signature is in store_date"""
            self.check_store()
            item = self.find_item(date_signature)
            return item

        def check_store(self) -> list:
            """Tries to open store_date file"""
            try:
                with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                    data_list = json.load(file)
            except json.JSONDecodeError as exception:
                raise VaccineManagementException(self.__ERROR_MESSAGE_JSON_DECODE) from exception
            except FileNotFoundError as exception:
                raise VaccineManagementException(self.__ERROR_MESSAGE_FILE_NOT_FOUND) from exception
            return data_list

    __instance = None

    def __new__(cls):
        if not AppointmentJsonStore.__instance:
            AppointmentJsonStore.__instance = AppointmentJsonStore.__AppointmentJsonStore()
        return AppointmentJsonStore.__instance
