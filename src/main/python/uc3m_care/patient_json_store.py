import json

from .json_store import JsonStore
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException
from .vaccine_manager_config import JSON_FILES_PATH


class PatientJsonStore(JsonStore):

    def __init__(self):
        pass

    def save_store(self, data: VaccinePatientRegister) -> True:
        """Method for saving the patients store"""
        patient_store = JSON_FILES_PATH + "store_patient.json"
        # first read the file
        data_list = self.load_store(patient_store)

        found = False
        # Buscamos el patient_id
        item = self.find_store(data_list, data.patient_id, "_VaccinePatientRegister__patient_id")
        # Si lo encontramos, buscamos el registration_type y el full_name
        if item is not None:
            if (item["_VaccinePatientRegister__registration_type"] == data.vaccine_type) and \
                    (item["_VaccinePatientRegister__full_name"] == data.full_name):
                found = True

        if found is False:
            data_list.append(data.__dict__)

        self.save(data_list, patient_store)

        if found is True:
            raise VaccineManagementException("patien_id is registered in store_patient")

        return True

    def find_patient_store(self, data: dict) -> VaccinePatientRegister:
        file_store = JSON_FILES_PATH + "store_patient.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
            item_found = self.find_store(data_list, data["PatientSystemID"], "_VaccinePatientRegister__patient_sys_id")

        return item_found
