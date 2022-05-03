"""Module vaccine_patient_register"""
import hashlib
import json
from datetime import datetime
from freezegun import freeze_time

from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.data.attribute.attribute_uuid import Uuid
from uc3m_care.data.attribute.attribute_name_surname import NameSurname
from uc3m_care.data.attribute.attribute_registration_type import RegistrationType
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_age import Age
#from uc3m_care.storage.patient_json_store import PatientJsonStore
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class VaccinePatientRegister:
    """Class representing the register of the patient in the system"""
    KEY_LABEL_PATIENT_ID = "_VaccinePatientRegister__patient_id"
    KEY_LABEL_FULL_NAME = "_VaccinePatientRegister__full_name"
    KEY_LABEL_REGISTRATION_TYPE = "_VaccinePatientRegister__registration_type"
    KEY_LABEL_PHONE_NUMBER = "_VaccinePatientRegister__phone_number"
    KEY_LABEL_AGE = "_VaccinePatientRegister__age"
    KEY_LABEL_TIME_STAMP = "_VaccinePatientRegister__time_stamp"
    KEY_LABEL_PATIENT_SYSTEM_ID = "_VaccinePatientRegister__patient_sys_id"
    __ERROR_MESSAGE_PATIENT_SYS_ID_INCORRECT = "Patient's data have been manipulated"
    __ERROR_MESSAGE_PATIENT_SYS_ID_NOT_FOUND = "patient_system_id not found"

    #pylint: disable=too-many-arguments
    def __init__(self, patient_id: str, full_name: str, registration_type: str, phone_number: str, age: str) -> None:
        self.__patient_id = Uuid(patient_id).value
        self.__full_name = NameSurname(full_name).value
        self.__registration_type = RegistrationType(registration_type).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__age = Age(age).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)
        #self.__time_stamp = 1645542405.232003
        self.__patient_sys_id = hashlib.md5(self.__str__().encode()).hexdigest()

    def __str__(self) -> str:
        return "VaccinePatientRegister:" + json.dumps(self.__dict__)

    @property
    def full_name(self) -> str:
        """Property representing the name and the surname of
        the person who request the registration"""
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        self.__full_name = NameSurname(value).value

    @property
    def vaccine_type(self) -> str:
        """Property representing the type vaccine"""
        return self.__registration_type

    @vaccine_type.setter
    def vaccine_type(self, value: str) -> None:
        self.__registration_type = RegistrationType(value).value

    @property
    def phone_number(self) -> str:
        """Property representing the requester's phone number"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value: str) -> None:
        self.__phone_number = PhoneNumber(value).value

    @property
    def patient_id(self) -> str:
        """Property representing the requester's UUID"""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value: str) -> None:
        self.__patient_id = Uuid(value).value

    @property
    def time_stamp(self) -> float:
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def patient_system_id(self) -> str:
        """Returns the md5 signature"""
        return self.__patient_sys_id

    @property
    def patient_age(self) -> str:
        """Returns the patient's age"""
        return self.__age

    @property
    def patient_sys_id(self) -> str:
        """Property representing the md5 generated"""
        return self.__patient_sys_id

    @classmethod
    def check_patient_sys_id(cls, patient_system_id: str) -> str:
        file_store = JSON_FILES_PATH + "store_patient.json"
        """
        my_store = PatientJsonStore()
        item = my_store.find_patient_store(patient_system_id)
        """
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)

        found = False
        for item in data_list:
            if item[cls.KEY_LABEL_PATIENT_SYSTEM_ID] == patient_system_id:
                found = True

                guid = item[cls.KEY_LABEL_PATIENT_ID]
                name = item[cls.KEY_LABEL_FULL_NAME]
                reg_type = item[cls.KEY_LABEL_REGISTRATION_TYPE]
                phone = item[cls.KEY_LABEL_PHONE_NUMBER]
                age = item[cls.KEY_LABEL_AGE]
                # set the date when the patient was registered for checking the md5
                patient_timestamp = item[cls.KEY_LABEL_TIME_STAMP]
                freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
                freezer.start()
                patient = cls(guid, name, reg_type, phone, age)
                freezer.stop()

                if patient.patient_system_id != patient_system_id:
                    raise VaccineManagementException(cls.__ERROR_MESSAGE_PATIENT_SYS_ID_INCORRECT)
        if not found:
            raise VaccineManagementException(cls.__ERROR_MESSAGE_PATIENT_SYS_ID_NOT_FOUND)
        """
        # retrieve the patients data
        guid = item["_VaccinePatientRegister__patient_id"]
        name = item["_VaccinePatientRegister__full_name"]
        reg_type = item["_VaccinePatientRegister__registration_type"]
        phone = item["_VaccinePatientRegister__phone_number"]
        age = item["_VaccinePatientRegister__age"]
        # set the date when the patient was registered for checking the md5
        patient_timestamp = item["_VaccinePatientRegister__time_stamp"]
        freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
        freezer.start()
        patient = cls(guid, name, reg_type, phone, age)
        freezer.stop()
        # comprobamos si el patient_system_id generado coincide con el recibido
        if patient.patient_system_id != patient_system_id:
            raise VaccineManagementException("Patient's data have been manipulated")
        """
        return guid
