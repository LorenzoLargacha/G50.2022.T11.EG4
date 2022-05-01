import json

from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class JsonParser:
    _key_list = []
    _key_error_message = []
    def __init__(self, input_file):
        self._json_content = self._read_json_file(input_file)
        self._validate_key_labels()

    def _read_json_file(self, input_file: str) -> dict:
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exception:
            # file is not found
            raise VaccineManagementException("File is not found") from exception
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data

    def _validate_key_labels(self) -> None:
        """ checking all the levels of the input json file"""
        i = 0
        for key in self._key_list:
            if not key in self._json_content.keys():
                raise VaccineManagementException(self._key_error_message[i])
            i = i+1
        #if not ("PatientSystemID" in self._json_content.keys()):
            #raise VaccineManagementException("Bad label patient_id")
        #if not ("ContactPhoneNumber" in self._json_content.keys()):
            #raise VaccineManagementException("Bad label contact phone")

    @property
    def json_content(self):
        return self._json_content