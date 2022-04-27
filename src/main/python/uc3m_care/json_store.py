import json
from datetime import datetime
from .vaccine_patient_register import VaccinePatientRegister
from .vaccination_appoinment import VaccinationAppoinment
from .vaccine_management_exception import VaccineManagementException
from .vaccine_manager_config import JSON_FILES_PATH

class JsonStore():
    def __init__(self):
        pass

    @staticmethod
    def save_store(data: VaccinePatientRegister) -> True:
        """Medthod for saving the patients store"""
        patient_store = JSON_FILES_PATH + "store_patient.json"
        # first read the file
        data_list = JsonStore.load_store(patient_store)

        found = False
        for item in data_list:
            if item["_VaccinePatientRegister__patient_id"] == data.patient_id:
                if (item["_VaccinePatientRegister__registration_type"] == data.vaccine_type) and \
                        (item["_VaccinePatientRegister__full_name"] == data.full_name):
                    found = True

        if found is False:
            data_list.append(data.__dict__)

        try:
            with open(patient_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

        if found is True:
            raise VaccineManagementException("patien_id is registered in store_patient")
        return True

    @staticmethod
    def load_store(file_store):
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
    def save_fast(data: dict) -> None:
        """Method for saving the patients store"""
        patients_store = JSON_FILES_PATH + "store_patient.json"
        with open(patients_store, "r+", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
            data_list.append(data.__dict__)
            file.seek(0)
            json.dump(data_list, file, indent=2)

    @staticmethod
    def save_store_date(date: VaccinationAppoinment) -> None:
        """Saves the appoinment into a file"""
        file_store_date = JSON_FILES_PATH + "store_date.json"
        # first read the file
        data_list = JsonStore.load_store(file_store_date)

        # append the date
        data_list.append(date.__dict__)

        try:
            with open(file_store_date, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

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
        try:
            with open(file_store_vaccine, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

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
