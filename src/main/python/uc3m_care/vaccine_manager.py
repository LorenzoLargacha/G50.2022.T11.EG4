"""Module """
import datetime
import json
from datetime import datetime
from freezegun import freeze_time

from uc3m_care.storage.patient_json_store import PatientJsonStore
from uc3m_care.storage.appointment_json_store import AppointmentJsonStore
from uc3m_care.storage.vaccine_json_store import VaccineJsonStore

from uc3m_care.data.vaccine_log import VaccineLog
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.vaccination_appoinment import VaccinationAppoinment

from uc3m_care.data.attribute.attribute_system_id import SystemId
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber


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
        my_store_patient = PatientJsonStore()
        my_store_patient.save_store_patient(my_patient)

        return my_patient.patient_sys_id

    def get_vaccine_date(self, input_file: str) -> str:
        """Gets an appoinment for a registered patient"""

        #data = self.read_json_file(input_file)

        #self.validate_key_labels(data)
        #SystemId(data["PatientSystemID"])
        #PhoneNumber(data["ContactPhoneNumber"])

        #item_found = self.find_patient_store(data)
        #my_store = PatientJsonStore()
        #item_found = my_store.find_patient_store(data)

        #if item_found is None:
            #raise VaccineManagementException("patient_system_id not found")

        #guid = self.check_patient_sys_id(data, item_found)

        my_sign = VaccinationAppoinment(input_file)

        # save the date in store_date.json
        my_store_date = AppointmentJsonStore()
        my_store_date.add_item(my_sign)

        return my_sign.date_signature

    def register_vaccine_patient(self, date_signature: str) -> True:
        """Register the vaccination of the patient"""
        #self.validate_date_signature(date_signature)
        #DateSignature(date_signature)

        my_vaccine_log = VaccineLog(date_signature)
        #date_signature = my_vaccine_log.date_signature

        #date_time = self.find_date_signature(date_signature)
        #my_store_date = JsonStore()
        my_store_date = AppointmentJsonStore()
        item = my_store_date.find_date_signature(date_signature)

        if item is None:
            raise VaccineManagementException("date_signature is not found")

        date_time = item["_VaccinationAppoinment__appoinment_date"]

        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(date_time).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")

        #self.save_vaccine(date_signature)
        my_store_vaccine = VaccineJsonStore()
        my_store_vaccine.add_item(my_vaccine_log)

        return True



