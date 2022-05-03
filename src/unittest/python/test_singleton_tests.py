"""Module for testing singleton"""
import unittest

from uc3m_care.storage.appointment_json_store import AppointmentJsonStore


class SingletonTests(unittest.TestCase):
    """Class for testing singleton"""
    def test_singleton_appointment_json_store(self):
        """Method for testing singleton on AppointmentJsonStore"""
        my_store_1 = AppointmentJsonStore()
        my_store_2 = AppointmentJsonStore()
        my_store_3 = AppointmentJsonStore()
        my_store_4 = AppointmentJsonStore()

        self.assertEqual(my_store_1, my_store_2)
        self.assertEqual(my_store_1, my_store_3)
        self.assertEqual(my_store_1, my_store_4)


if __name__ == '__main__':
    unittest.main()
