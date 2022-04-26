"""MODULE: access_request. Contains the access request class"""
import hashlib
import uuid
import re
import json
from datetime import datetime

from .vaccine_management_exception import VaccineManagementException

class VaccinePatientRegister:
    """Class representing the register of the patient in the system"""
    #pylint: disable=too-many-arguments
    def __init__(self, patient_id: str, full_name: str, registration_type: str, phone_number: str, age: str) -> None:
        self.__patient_id = self.validate_guid(patient_id)
        self.__full_name = self.validate_name_surname(full_name)
        self.__registration_type = self.validate_registration_type(registration_type)
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
        self.__full_name = self.validate_name_surname(value)

    @property
    def vaccine_type(self) -> str:
        """Property representing the type vaccine"""
        return self.__registration_type
    @vaccine_type.setter
    def vaccine_type(self, value: str) -> None:
        self.__registration_type = self.validate_registration_type(value)

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
        self.__patient_id = self.validate_guid(value)

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

    def validate_guid(self, patient_id: str) -> str:
        "Method for validating uuid  v4"
        try:
            my_uuid = uuid.UUID(patient_id)
            uuid_pattern = re.compile(r"^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]" +
                                 "{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$",
                                 re.IGNORECASE)
            result = uuid_pattern.fullmatch(my_uuid.__str__())
            if not result:
                raise VaccineManagementException("UUID invalid")
        except ValueError as val_er:
            raise VaccineManagementException("Id received is not a UUID") from val_er
        return patient_id

    def validate_registration_type(self, registration_type: str) -> str:
        registration_type_pattern = re.compile(r"(Regular|Family)")
        result = registration_type_pattern.fullmatch(registration_type)
        if not result:
            raise VaccineManagementException("Registration type is nor valid")
        return registration_type

    def validate_name_surname(self, name_surname: str) -> str:
        name_surname_pattern = re.compile(r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$")
        result = name_surname_pattern.fullmatch(name_surname)
        if not result:
            raise VaccineManagementException("name surname is not valid")
        return name_surname

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

