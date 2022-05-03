"""Module appointment_json_parser"""
from uc3m_care.parser.json_parser import JsonParser


class AppointmentJsonParser(JsonParser):
    """Clase hija de JsonParser con los atributos del input file"""
    _key_list = ["PatientSystemID", "ContactPhoneNumber"]
    _key_error_message = ["Bad label patient_id", "Bad label contact phone"]
