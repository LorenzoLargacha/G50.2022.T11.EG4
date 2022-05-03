"""Module vaccine_log"""
from datetime import datetime

from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.vaccination_appoinment import VaccinationAppoinment
from uc3m_care.storage.appointment_json_store import AppointmentJsonStore
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class VaccineLog:
    """Clase que representa la firma y fecha de vacunación de un paciente"""
    KEY_LABEL_APPOINMENT_DATE = "_VaccinationAppoinment__appoinment_date"
    __ERROR_MESSAGE_DATE_SIGNATURE_NOT_FOUND = "date_signature is not found"
    __ERROR_MESSAGE_NOT_THE_DATE = "Today is not the date"

    def __init__(self, date_signature: str) -> None:
        self.__date_signature = DateSignature(date_signature).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)

    @property
    def date_signature(self) -> str:
        """Property that represents the signature of a vaccine log"""
        return self.__date_signature

    @date_signature.setter
    def date_signature(self, value: str) -> None:
        self.__date_signature = DateSignature(value).value

    @property
    def time_stamp(self) -> float:
        """Property that represents the time stamp of a vaccine log"""
        return self.__time_stamp

    @time_stamp.setter
    def time_stamp(self, value: float) -> None:
        self.__time_stamp = value

    def check_date(self) -> None:
        """Checks if a vaccination appointment is registered"""
        item = self.check_date_signature()
        date_time = item[self.KEY_LABEL_APPOINMENT_DATE]
        self.is_the_date(date_time)

    def check_date_signature(self) -> VaccinationAppoinment:
        """Checks if this date is in store_date"""
        my_store_date = AppointmentJsonStore()
        item = my_store_date.find_date_signature(self.__date_signature)
        if item is None:
            raise VaccineManagementException(self.__ERROR_MESSAGE_DATE_SIGNATURE_NOT_FOUND)
        return item

    def is_the_date(self, date_time: float) -> None:
        """Checks if the date of the appointment is today"""
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(date_time).date()
        if date_patient != today:
            raise VaccineManagementException(self.__ERROR_MESSAGE_NOT_THE_DATE)
