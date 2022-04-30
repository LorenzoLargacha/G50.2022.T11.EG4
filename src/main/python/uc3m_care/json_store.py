import json
from datetime import datetime
from .vaccine_patient_register import VaccinePatientRegister
from .vaccination_appoinment import VaccinationAppoinment
from .vaccine_management_exception import VaccineManagementException
from .vaccine_log import VaccineLog
from .vaccine_manager_config import JSON_FILES_PATH


class JsonStore:
    _FILE_PATH = ""
    _ID_FIELD = ""

    def __init__(self):
        pass

    def save_store(self, data_list: list, file_store: str) -> None:
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

    def load_store(self, file_store: str) -> list:
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data_list

    def find_item(self, data_list: list, item_to_find: str, key: str) -> dict:
        for item in data_list:
            if item[key] == item_to_find:
                return item
        return None

    def add_item(self, item: dict, file_store_date: str) -> None:
        # first read the file
        data_list = self.load_store(file_store_date)
        # append the item
        data_list.append(item.__dict__)
        # save data into file
        self.save_store(data_list, file_store_date)

    def save_vaccine(self, vaccine_log: VaccineLog) -> None:
        file_store_vaccine = JSON_FILES_PATH + "store_vaccine.json"
        self.add_item(vaccine_log, file_store_vaccine)
