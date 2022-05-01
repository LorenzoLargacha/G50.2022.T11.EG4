import json
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class JsonStore:
    # Ruta fichero store
    _FILE_PATH = ""
    # Key a buscar
    _ID_FIELD = ""

    __ERROR_MESSAGE_FILE_NOT_FOUND = "Wrong file or file path"
    __ERROR_MESSAGE_JSON_DECODE = "JSON Decode Error - Wrong JSON Format"

    def __init__(self):
        pass

    def save_store(self, data_list: list) -> None:
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException(self.__ERROR_MESSAGE_FILE_NOT_FOUND) from exception

    def load_store(self) -> list:
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException(self.__ERROR_MESSAGE_JSON_DECODE) from exception
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
