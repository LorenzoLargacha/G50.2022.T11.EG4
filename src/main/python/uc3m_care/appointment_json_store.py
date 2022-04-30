import json

from .json_store import JsonStore
from .vaccination_appoinment import VaccinationAppoinment
from .vaccine_management_exception import VaccineManagementException
from .vaccine_manager_config import JSON_FILES_PATH


class AppointmentJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_date.json"
    _ID_FIELD = "_VaccinationAppoinment__date_signature"

    def __init__(self):
        pass

    def save_store_date(self, date: VaccinationAppoinment) -> None:
        """Saves the appoinment into a file"""
        self.add_item(date)

    def find_date_signature(self, date_signature: str) -> VaccinationAppoinment:
        # check if this date is in store_date
        data_list = self.check_store()
        # search this date_signature
        item = self.find_item(data_list, date_signature, self._ID_FIELD)

        return item

    def check_store(self) -> list:
        # first read the file
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        except FileNotFoundError as exception:
            raise VaccineManagementException("Store_date not found") from exception
        return data_list
