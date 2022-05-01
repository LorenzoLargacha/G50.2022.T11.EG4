""" Module """
from datetime import datetime
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.storage.appointment_json_store import AppointmentJsonStore
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class VaccineLog:
    def __init__(self, date_signature) -> None:
        self.__date_signature = DateSignature(date_signature).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)

    @property
    def date_signature(self):
        return self.__date_signature

    @date_signature.setter
    def date_signature(self, value):
        self.__date_signature = DateSignature(value).value

    @property
    def time_stamp (self):
        return self.__timestamp

    @time_stamp.setter
    def time_stamp (self, value):
        self.__time_stamp = value

    def check_date(self):
        item = self.check_date_signature()
        date_time = item["_VaccinationAppoinment__appoinment_date"]
        self.is_the_date(date_time)

    def check_date_signature(self):
        # check if this date is in store_date
        my_store_date = AppointmentJsonStore()
        item = my_store_date.find_date_signature(self.__date_signature)
        if item is None:
            raise VaccineManagementException("date_signature is not found")
        return item

    def is_the_date(self, date_time):
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(date_time).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")

