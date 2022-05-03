"""Module vaccination_appoinment"""
import hashlib
from datetime import datetime

from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_system_id import SystemId
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser


class VaccinationAppoinment:
    """Class representing an appoinment  for the vaccination of a patient"""
    KEY_JSON_PATIENT_SYSTEM_ID = "PatientSystemID"
    KEY_JSON_PHONE_NUMBER = "ContactPhoneNumber"
    __ALG = "SHA-256"
    __TYPE = "DS"

    def __init__(self, input_file: str) -> None:
        self.__json_content = AppointmentJsonParser(input_file).json_content
        self.__alg = self.__ALG
        self.__type = self.__TYPE
        self.__patient_sys_id = SystemId(self.__json_content[self.KEY_JSON_PATIENT_SYSTEM_ID]).value
        self.__phone_number = PhoneNumber(self.__json_content[self.KEY_JSON_PHONE_NUMBER]).value
        self.__patient_id = VaccinePatientRegister.check_patient_sys_id(self.__patient_sys_id)
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        days = 10
        if days == 0:
            self.__appoinment_date = 0
        else:
            # timestamp is represented in seconds.microseconds
            # age must be expressed in seconds to be added to the timestap
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
