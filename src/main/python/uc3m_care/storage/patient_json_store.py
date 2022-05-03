"""Module patient_json_store"""
from uc3m_care.storage.json_store import JsonStore
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH


class PatientJsonStore(JsonStore):
    """Clase hija de JsonStore con los atributos para store_patient"""
    _FILE_PATH = JSON_FILES_PATH + "store_patient.json"
    _ID_FIELD = "_VaccinePatientRegister__patient_id"

    __ERROR_MESSAGE_INVALID_OBJECT = "Invalid vaccine patient register object"
    __ERROR_MESSAGE_PATIENT_ID_REGISTERED = "patien_id is registered in store_patient"

    def __init__(self):
        pass

    def save_store_patient(self, patient: VaccinePatientRegister) -> True:
        """Saves a patient into a file"""
        if not isinstance(patient, VaccinePatientRegister):
            raise VaccineManagementException(self.__ERROR_MESSAGE_INVALID_OBJECT)

        found = False
        # Buscamos el patient_id
        item = self.find_item(patient.patient_id)
        # Si lo encontramos, buscamos el registration_type y el full_name
        if item is not None:
            if (item[VaccinePatientRegister.KEY_LABEL_REGISTRATION_TYPE] == patient.vaccine_type) and \
                    (item[VaccinePatientRegister.KEY_LABEL_FULL_NAME] == patient.full_name):
                found = True

        if found is False:
            self.add_item(patient)

        if found is True:
            raise VaccineManagementException(self.__ERROR_MESSAGE_PATIENT_ID_REGISTERED)

        return True

    def find_patient_store(self, patient_system_id: str) -> VaccinePatientRegister:
        """Looks for a patient_system_id in store_patient"""
        with open(self._FILE_PATH, "r", encoding="utf-8", newline=""):
            self._ID_FIELD = VaccinePatientRegister.KEY_LABEL_PATIENT_SYSTEM_ID
            item_found = self.find_item(patient_system_id)
            self._ID_FIELD = VaccinePatientRegister.KEY_LABEL_PATIENT_ID

        return item_found
