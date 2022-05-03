"""Module json_parser"""
import json

from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class JsonParser:
    """Clase que representa la solicitud de una cita de vacunación"""
    _key_list = []
    _key_error_message = []

    __ERROR_MESSAGE_FILE_NOT_FOUND = "File is not found"
    __ERROR_MESSAGE_JSON_DECODE = "JSON Decode Error - Wrong JSON Format"

    def __init__(self, input_file: str) -> None:
        self._json_content = self._read_json_file(input_file)
        self._validate_key_labels()

    def _read_json_file(self, input_file: str) -> dict:
        """Loads the contents of a json file"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exception:
            raise VaccineManagementException(self.__ERROR_MESSAGE_FILE_NOT_FOUND) from exception
        except json.JSONDecodeError as exception:
            raise VaccineManagementException(self.__ERROR_MESSAGE_JSON_DECODE) from exception
        return data

    def _validate_key_labels(self) -> None:
        """Checks all the levels of the input json file"""
        i = 0
        for key in self._key_list:
            if key not in self._json_content.keys():
                raise VaccineManagementException(self._key_error_message[i])
            i = i+1

    @property
    def json_content(self) -> dict:
        """Property that represents the content of a vaccine request"""
        return self._json_content
