"""Module """
import datetime
import uuid
import re
import json
from datetime import datetime
from freezegun import freeze_time
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException
from .vaccination_appoinment import VaccinationAppoinment
from .vaccine_manager_config import JSON_FILES_PATH

class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""
    def __init__(self):
        pass

    @staticmethod
    def validate_date_signature(date_signature: str) -> None:
        """Method for validating sha256 values"""
        date_signature_pattern = re.compile(r"[0-9a-fA-F]{64}$")
        result = date_signature_pattern.fullmatch(date_signature)
        if not result:
            raise VaccineManagementException("date_signature format is not valid")

    @staticmethod
    def save_store(data: VaccinePatientRegister) -> True:
        """Medthod for saving the patients store"""
        file_store = JSON_FILES_PATH + "store_patient.json"
        #first read the file
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
    def save_fast(data):
        """Method for saving the patients store"""
        patients_store = JSON_FILES_PATH + "store_patient.json"
        with open(patients_store, "r+", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
            data_list.append(data.__dict__)
            file.seek(0)
            json.dump(data_list, file, indent=2)

    @staticmethod
    def save_store_date(date):
        """Saves the appoinment into a file"""
        file_store_date = JSON_FILES_PATH + "store_date.json"
        # first read the file
        try:
            with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception

        #append the date
        data_list.append(date.__dict__)

        try:
            with open(file_store_date, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception


    #pylint: disable=too-many-arguments
    def request_vaccination_id (self, patient_id,
                                name_surname,
                                registration_type,
                                phone_number,
                                age):
        """Register the patinent into the patients file"""
        #self.validate_registration_type(registration_type)
        #self.validate_name_surname(name_surname)
        #self.validate_phone_number(phone_number)
        #self.validate_age(age)
        #if self.validate_guid(patient_id):
        my_patient = VaccinePatientRegister(patient_id,
                                            name_surname,
                                            registration_type,
                                            phone_number,
                                            age)

        self.save_store(my_patient)

        return my_patient.patient_sys_id


    def get_vaccine_date(self, input_file):
        """Gets an appoinment for a registered patient"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exception:
            # file is not found
            raise VaccineManagementException("File is not found") from exception
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception

        #check all the information
        try:
            patient_system_id_pattern = re.compile(r"[0-9a-fA-F]{32}$")
            result = patient_system_id_pattern.fullmatch(data["PatientSystemID"])
            if not result:
                raise VaccineManagementException("patient system id is not valid")
        except KeyError as exception:
            raise VaccineManagementException("Bad label patient_id") from exception

        try:
            VaccinePatientRegister.validate_phone_number(data["ContactPhoneNumber"])
        except KeyError as exception:
            raise VaccineManagementException("Bad label contact phone") from exception
        file_store = JSON_FILES_PATH + "store_patient.json"

        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_VaccinePatientRegister__patient_sys_id"] == data["PatientSystemID"]:
                found = True
                #retrieve the patients data
                guid = item["_VaccinePatientRegister__patient_id"]
                name = item["_VaccinePatientRegister__full_name"]
                reg_type = item["_VaccinePatientRegister__registration_type"]
                phone =item["_VaccinePatientRegister__phone_number"]
                patient_timestamp = item["_VaccinePatientRegister__time_stamp"]
                age = item["_VaccinePatientRegister__age"]
                #set the date when the patient was registered for checking the md5
                freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
                freezer.start()
                patient = VaccinePatientRegister(guid,name,reg_type,phone,age)
                freezer.stop()
                if patient.patient_system_id != data["PatientSystemID"]:
                    raise VaccineManagementException("Patient's data have been manipulated")

        if not found:
            raise VaccineManagementException("patient_system_id not found")

        my_sign = VaccinationAppoinment(guid, data["PatientSystemID"], data["ContactPhoneNumber"], 10)

        #save the date in store_date.json

        self.save_store_date(my_sign)

        return my_sign.date_signature

    def register_vaccine_patient(self, date_signature):
        """Register the vaccination of the patient"""
        self.validate_date_signature(date_signature)

        #check if this date is in store_date
        file_store_date = JSON_FILES_PATH + "store_date.json"
        # first read the file
        try:
            with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        except FileNotFoundError as exception:
            raise VaccineManagementException("Store_date not found") from exception
        #search this date_signature
        found = False
        for item in data_list:
            if item["_VaccinationAppoinment__date_signature"] == date_signature:
                found = True
                date_time = item["_VaccinationAppoinment__appoinment_date"]
        if not found:
            raise VaccineManagementException("date_signature is not found")

        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(date_time).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")

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
        return True
