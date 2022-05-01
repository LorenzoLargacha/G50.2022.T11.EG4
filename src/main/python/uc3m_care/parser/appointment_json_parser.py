from uc3m_care.parser.json_parser import JsonParser

class AppointmentJsonParser(JsonParser):
    _key_list = ["PatientSystemID", "ContactPhoneNumber"]
    _key_error_message = ["Bad label patient_id", "Bad label contact phone"]

