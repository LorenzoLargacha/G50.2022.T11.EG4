"""Module for testing singleton"""
import unittest

from uc3m_care.storage.patient_json_store import PatientJsonStore
from uc3m_care.storage.appointment_json_store import AppointmentJsonStore
from uc3m_care.storage.vaccine_json_store import VaccineJsonStore


class SingletonTests(unittest.TestCase):
    """Class for testing singleton"""
    def test_singleton_patient_json_store(self):
        """Method for testing singleton on PatientJsonStore"""
        my_store_1 = PatientJsonStore()
        my_store_2 = PatientJsonStore()
        my_store_3 = PatientJsonStore()
        my_store_4 = PatientJsonStore()

        self.assertEqual(my_store_1, my_store_2)
        self.assertEqual(my_store_1, my_store_3)
        self.assertEqual(my_store_1, my_store_4)

    def test_singleton_appointment_json_store(self):
        """Method for testing singleton on AppointmentJsonStore"""
        my_store_1 = AppointmentJsonStore()
        my_store_2 = AppointmentJsonStore()
        my_store_3 = AppointmentJsonStore()
        my_store_4 = AppointmentJsonStore()

        self.assertEqual(my_store_1, my_store_2)
        self.assertEqual(my_store_1, my_store_3)
        self.assertEqual(my_store_1, my_store_4)

    def test_singleton_vaccine_json_store(self):
        """Method for testing singleton on VaccineJsonStore"""
        my_store_1 = VaccineJsonStore()
        my_store_2 = VaccineJsonStore()
        my_store_3 = VaccineJsonStore()
        my_store_4 = VaccineJsonStore()

        self.assertEqual(my_store_1, my_store_2)
        self.assertEqual(my_store_1, my_store_3)
        self.assertEqual(my_store_1, my_store_4)


if __name__ == '__main__':
    unittest.main()
