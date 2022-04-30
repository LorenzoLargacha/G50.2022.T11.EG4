"""Contains the class Vaccination Appoinment"""
from datetime import datetime
import hashlib
import json

from uc3m_care import VaccineManagementException


class VaccinationAppoinment:
    """Class representing an appoinment  for the vaccination of a patient"""

    def __init__(self, guid: str, patient_sys_id: str, patient_phone_number: str, days: int) -> None:
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_id = guid
        self.__patient_sys_id = patient_sys_id
        self.__phone_number = patient_phone_number
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if days == 0:
            self.__appoinment_date = 0
        else:
            #timestamp is represneted in seconds.microseconds
            #age must be expressed in senconds to be added to the timestap
            self.__appoinment_date = self.__issued_at + (days * 24 * 60 * 60)
        self.__date_signature = self.vaccination_signature


    def __signature_string(self) -> str:
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg +",typ:" + self.__type +",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appoinment_date.__str__() + "}"

    @property
    def patient_id(self) -> str:
        """Property that represents the guid of the patient"""
        return self.__patient_id
    @patient_id.setter
    def patient_id(self, value: str) -> None:
        self.__patient_id = value

    @property
    def patient_sys_id(self) -> str:
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id
    @patient_sys_id.setter
    def patient_sys_id(self, value: str) -> None:
        self.__patient_sys_id = value

    @property
    def phone_number(self) -> str:
        """Property that represents the phone number of the patient"""
        return self.__phone_number
    @phone_number.setter
    def phone_number(self, value: str) -> None:
        self.__phone_number = value

    @property
    def vaccination_signature(self) -> str:
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self) -> float:
        """Returns the issued at value"""
        return self.__issued_at
    @issued_at.setter
    def issued_at(self, value: float) -> None:
        self.__issued_at = value

    @property
    def appoinment_date(self) -> float:
        """Returns the vaccination date"""
        return self.__appoinment_date

    @property
    def date_signature(self) -> str:
        """Returns the SHA256 """
        return self.__date_signature

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
