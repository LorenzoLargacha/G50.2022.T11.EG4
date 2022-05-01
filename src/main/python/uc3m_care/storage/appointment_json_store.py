import json

from uc3m_care.storage.json_store import JsonStore
from uc3m_care.data.vaccination_appoinment import VaccinationAppoinment
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH


class AppointmentJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_date.json"
    _ID_FIELD = "_VaccinationAppoinment__date_signature"

    __ERROR_MESSAGE_INVALID_APPOINMENT_OBJ = "Invalid vaccination appointment object"
    __ERROR_MESSAGE_FILE_NOT_FOUND = "Store_date not found"

    def __init__(self):
        pass

    def add_item(self, date: VaccinationAppoinment) -> None:
        """Saves the appoinment into a file"""
        if not isinstance(date, VaccinationAppoinment):
            raise VaccineManagementException(self.__ERROR_MESSAGE_INVALID_APPOINMENT_OBJ)
        super().add_item(date)

    def find_date_signature(self, date_signature: str) -> VaccinationAppoinment:
        # check if this date is in store_date
        self.check_store()
        # search this date_signature
        item = self.find_item(date_signature)

        return item

    def check_store(self) -> list:
        # first read the file
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as exception:
            raise VaccineManagementException(self.__ERROR_MESSAGE_JSON_DECODE) from exception
        except FileNotFoundError as exception:
            raise VaccineManagementException(self.__ERROR_MESSAGE_FILE_NOT_FOUND) from exception
        return data_list
