"""Module vaccine_manager"""
from uc3m_care.storage.patient_json_store import PatientJsonStore
from uc3m_care.storage.appointment_json_store import AppointmentJsonStore
from uc3m_care.storage.vaccine_json_store import VaccineJsonStore

from uc3m_care.data.vaccine_log import VaccineLog
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.vaccination_appoinment import VaccinationAppoinment


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
        """Register a patinent"""
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
        my_sign = VaccinationAppoinment(input_file)

        my_store_date = AppointmentJsonStore()
        my_store_date.add_item(my_sign)

        return my_sign.date_signature

    def register_vaccine_patient(self, date_signature: str) -> True:
        """Registers the vaccination of a patient"""
        my_vaccine_log = VaccineLog(date_signature)
        my_vaccine_log.check_date()

        my_store_vaccine = VaccineJsonStore()
        my_store_vaccine.add_item(my_vaccine_log)

        return True
