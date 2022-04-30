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
        file_store_date = JSON_FILES_PATH + "store_date.json"
        self.add_item(date, self._FILE_PATH)

    def find_date_signature(self, date_signature: str) -> float:
        # check if this date is in store_date
        file_store_date = JSON_FILES_PATH + "store_date.json"
        data_list = self.check_store(self._FILE_PATH)
        # search this date_signature
        item = self.find_item(data_list, date_signature, self._ID_FIELD)

        if item is None:
            raise VaccineManagementException("date_signature is not found")

        date_time = item["_VaccinationAppoinment__appoinment_date"]
        return date_time

    def check_store(self, file_store_date):
        # first read the file
        try:
            with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        except FileNotFoundError as exception:
            raise VaccineManagementException("Store_date not found") from exception
        return data_list
