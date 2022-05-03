"""Module json_store"""
import json
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class JsonStore:
    """Clase con los métodos para modificar los stores"""
    # Ruta fichero store
    _FILE_PATH = ""
    # Key a buscar
    _ID_FIELD = ""

    __ERROR_MESSAGE_FILE_NOT_FOUND = "Wrong file or file path"
    __ERROR_MESSAGE_JSON_DECODE = "JSON Decode Error - Wrong JSON Format"

    def __init__(self):
        pass

    def save_store(self, data_list: list) -> None:
        """Saves a data list into a json file"""
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException(self.__ERROR_MESSAGE_FILE_NOT_FOUND) from exception

    def load_store(self) -> list:
        """Loads the contents of a json file into a data list"""
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found, so  init my data_list
            data_list = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException(self.__ERROR_MESSAGE_JSON_DECODE) from exception
        return data_list

    def find_item(self, item_to_find: str) -> any:
        """Looks for a value from an item key in a json file"""
        data_list = self.load_store()
        for item in data_list:
            if item[self._ID_FIELD] == item_to_find:
                return item
        return None

    def add_item(self, item: object) -> None:
        """Adds an item to a json file"""
        data_list = self.load_store()
        data_list.append(item.__dict__)
        self.save_store(data_list)
