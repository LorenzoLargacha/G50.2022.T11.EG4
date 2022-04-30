import json

from .json_store import JsonStore
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException
from .vaccine_manager_config import JSON_FILES_PATH


class PatientJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_patient.json"
    _ID_FIELD = "_VaccinePatientRegister__patient_id"

    def __init__(self):
        pass

    def save_store_patient(self, patient: VaccinePatientRegister) -> True:
        """Method for saving the patients store"""
        found = False
        # Buscamos el patient_id
        item = self.find_item(patient.patient_id)
        # Si lo encontramos, buscamos el registration_type y el full_name
        if item is not None:
            if (item["_VaccinePatientRegister__registration_type"] == patient.vaccine_type) and \
                    (item["_VaccinePatientRegister__full_name"] == patient.full_name):
                found = True

        if found is False:
            # Solo hago save si el paciente no estaba almacenado
            self.add_item(patient)

        if found is True:
            raise VaccineManagementException("patien_id is registered in store_patient")

        return True

    def find_patient_store(self, data: dict) -> VaccinePatientRegister:
        with open(self._FILE_PATH, "r", encoding="utf-8", newline=""):
            self._ID_FIELD = "_VaccinePatientRegister__patient_sys_id"
            item_found = self.find_item(data["PatientSystemID"])
            self._ID_FIELD = "_VaccinePatientRegister__patient_id"

        return item_found
