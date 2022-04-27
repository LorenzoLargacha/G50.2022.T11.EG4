import json
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException
from .vaccine_manager_config import JSON_FILES_PATH

class JsonStore():
    def __init__(self):
        pass

    @staticmethod
    def save_store(data: VaccinePatientRegister) -> True:
        """Medthod for saving the patients store"""
        file_store = JSON_FILES_PATH + "store_patient.json"
        # first read the file
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception

        found = False
        for item in data_list:
            if item["_VaccinePatientRegister__patient_id"] == data.patient_id:
                if (item["_VaccinePatientRegister__registration_type"] == data.vaccine_type) and \
                        (item["_VaccinePatientRegister__full_name"] == data.full_name):
                    found = True

        if found is False:
            data_list.append(data.__dict__)

        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

        if found is True:
            raise VaccineManagementException("patien_id is registered in store_patient")
        return True

    @staticmethod
    def find_patient_store(data: dict) -> VaccinePatientRegister:
        file_store = JSON_FILES_PATH + "store_patient.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_VaccinePatientRegister__patient_sys_id"] == data["PatientSystemID"]:
                return item
        return None
