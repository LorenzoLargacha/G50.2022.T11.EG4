"""Module """
import datetime
import json
from datetime import datetime
from freezegun import freeze_time

from .json_store import JsonStore
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException
from .vaccination_appoinment import VaccinationAppoinment
from .vaccine_manager_config import JSON_FILES_PATH

from .attribute_system_id import SystemId
from .attribute_phone_number import PhoneNumber
from .attribute_date_signature import DateSignature


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""
    def __init__(self):
        pass

    #pylint: disable=too-many-arguments
    def request_vaccination_id(self, patient_id: str,
                               name_surname: str,
                               registration_type: str,
                               phone_number: str,
                               age: str) -> str:
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
        my_store = JsonStore()
        my_store.save_store(my_patient)

        return my_patient.patient_sys_id


    def get_vaccine_date(self, input_file: str) -> str:
        """Gets an appoinment for a registered patient"""

        data = self.read_json_file(input_file)

        self.validate_key_labels(data)
        SystemId(data["PatientSystemID"])
        PhoneNumber(data["ContactPhoneNumber"])

        #item_found = self.find_patient_store(data)
        my_store = JsonStore()
        item_found = my_store.find_patient_store(data)

        if item_found is None:
            raise VaccineManagementException("patient_system_id not found")
        guid = self.check_patient_sys_id(data, item_found)

        my_sign = VaccinationAppoinment(guid, data["PatientSystemID"], data["ContactPhoneNumber"], 10)

        # save the date in store_date.json
        #self.save_store_date(my_sign)
        my_store_date = JsonStore()
        my_store_date.save_store_date(my_sign)

        return my_sign.date_signature

    def read_json_file(self, input_file: str) -> str:
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exception:
            # file is not found
            raise VaccineManagementException("File is not found") from exception
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data

    def check_patient_sys_id(self, data: dict, item: VaccinePatientRegister) -> str:
        # retrieve the patients data
        guid = item["_VaccinePatientRegister__patient_id"]
        name = item["_VaccinePatientRegister__full_name"]
        reg_type = item["_VaccinePatientRegister__registration_type"]
        phone = item["_VaccinePatientRegister__phone_number"]
        patient_timestamp = item["_VaccinePatientRegister__time_stamp"]
        age = item["_VaccinePatientRegister__age"]
        # set the date when the patient was registered for checking the md5
        freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
        freezer.start()
        patient = VaccinePatientRegister(guid, name, reg_type, phone, age)
        freezer.stop()
        if patient.patient_system_id != data["PatientSystemID"]:
            raise VaccineManagementException("Patient's data have been manipulated")
        return guid

    def validate_key_labels(self, label_list):
        """ checking all the levels of the input json file"""
        if not ("PatientSystemID" in label_list.keys()):
            raise VaccineManagementException("Bad label patient_id")
        if not ("ContactPhoneNumber" in label_list.keys()):
            raise VaccineManagementException("Bad label contact phone")
        return label_list

    def register_vaccine_patient(self, date_signature: str) -> True:
        """Register the vaccination of the patient"""
        #self.validate_date_signature(date_signature)
        DateSignature(date_signature)

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
