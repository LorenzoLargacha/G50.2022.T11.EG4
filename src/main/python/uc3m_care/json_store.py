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

    def save_store(self, data_list: list) -> None:
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

    def load_store(self) -> list:
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data_list

    def find_item(self, item_to_find: str) -> any:
        # Primero cargamos la lista
        data_list = self.load_store()
        # Luego buscamos
        for item in data_list:
            if item[self._ID_FIELD] == item_to_find:
                return item
        return None

    def add_item(self, item: object) -> None:
        # first read the file
        data_list = self.load_store()
        # append the item
        data_list.append(item.__dict__)
        # save data into file
        self.save_store(data_list)
