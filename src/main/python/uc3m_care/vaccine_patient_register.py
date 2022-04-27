"""MODULE: access_request. Contains the access request class"""
import hashlib
import re
import json
from datetime import datetime

from .vaccine_management_exception import VaccineManagementException
from .attribute_uuid import Uuid
from .attribute_name_surname import NameSurname
from .attribute_registration_type import RegistrationType

class VaccinePatientRegister:
    """Class representing the register of the patient in the system"""
    #pylint: disable=too-many-arguments
    def __init__(self, patient_id: str, full_name: str, registration_type: str, phone_number: str, age: str) -> None:
        self.__patient_id = Uuid(patient_id).value
        self.__full_name = NameSurname(full_name).value
        self.__registration_type = RegistrationType(registration_type).value
        self.__phone_number = self.validate_phone_number(phone_number)
        self.__age = self.validate_age(age)
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
        self.__phone_number = self.validate_phone_number(value)

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

    def validate_age(self, age: str) -> str:
        if age.isnumeric():
            if int(age) < 6 or int(age) > 125:
                raise VaccineManagementException("age is not valid")
        else:
            raise VaccineManagementException("age is not valid")
        return age

    @staticmethod
    def validate_phone_number(phone_number: str) -> str:
        phone_number_pattern = re.compile(r"^(\+)[0-9]{11}")
        result = phone_number_pattern.fullmatch(phone_number)
        if not result:
            raise VaccineManagementException("phone number is not valid")
        return phone_number

