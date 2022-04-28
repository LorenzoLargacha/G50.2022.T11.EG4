import json
from datetime import datetime
from .vaccine_patient_register import VaccinePatientRegister
from .vaccination_appoinment import VaccinationAppoinment
from .vaccine_management_exception import VaccineManagementException
from .vaccine_manager_config import JSON_FILES_PATH

class JsonStore():
    def __init__(self):
        pass

    def save_store(self, data: VaccinePatientRegister) -> True:
        """Medthod for saving the patients store"""
        patient_store = JSON_FILES_PATH + "store_patient.json"
        # first read the file
        data_list = JsonStore.load_store(patient_store)

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

        JsonStore.save(data_list, patient_store)

        if found is True:
            raise VaccineManagementException("patien_id is registered in store_patient")
        return True

    @staticmethod
    def save(data_list, patient_store):
        try:
            with open(patient_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

    @staticmethod
    def load_store(file_store: str) -> list:
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data_list

    @staticmethod
    def save_store_date(date: VaccinationAppoinment) -> None:
        """Saves the appoinment into a file"""
        file_store_date = JSON_FILES_PATH + "store_date.json"
        # first read the file
        data_list = JsonStore.load_store(file_store_date)

        # append the date
        data_list.append(date.__dict__)

        JsonStore.save(data_list, file_store_date)

    @staticmethod
    def save_vaccine(date_signature: str) -> None:
        file_store_vaccine = JSON_FILES_PATH + "store_vaccine.json"
        try:
            with open(file_store_vaccine, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError as exception:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception

            # append the date
        data_list.append(date_signature.__str__())
        data_list.append(datetime.utcnow().__str__())
        JsonStore.save(data_list, file_store_vaccine)

    def find_store(self, data_list: list, item_to_find: str, key: str) -> any:
        for item in data_list:
            if item[key] == item_to_find:
                return item
        return None

    def find_patient_store(self, data: dict) -> VaccinePatientRegister:
        file_store = JSON_FILES_PATH + "store_patient.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        item_found = self.find_store(data_list, data["PatientSystemID"], "_VaccinePatientRegister__patient_sys_id")

        return item_found

    @staticmethod
    def find_date_signature(date_signature: str) -> float:
        # check if this date is in store_date
        file_store_date = JSON_FILES_PATH + "store_date.json"
        # first read the file
        try:
            with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        except FileNotFoundError as exception:
            raise VaccineManagementException("Store_date not found") from exception
        # search this date_signature
        found = False
        for item in data_list:
            if item["_VaccinationAppoinment__date_signature"] == date_signature:
                found = True
                date_time = item["_VaccinationAppoinment__appoinment_date"]
        if not found:
            raise VaccineManagementException("date_signature is not found")
        return date_time
