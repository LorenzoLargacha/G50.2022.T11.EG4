"""Module vaccine_json_store"""
from uc3m_care.storage.json_store import JsonStore
from uc3m_care.data.vaccine_log import VaccineLog
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH


class VaccineJsonStore(JsonStore):
    """Clase hija de JsonStore con los atributos para store_vaccine"""

    class __VaccineJsonStore(JsonStore):
        """Clase privada, patron singleton"""
        _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"

        __ERROR_MESSAGE_INVALID_OBJECT = "Invalid vaccine log object"

        def add_item(self, item: VaccineLog) -> None:
            """Saves a vaccine into a file"""
            if not isinstance(item, VaccineLog):
                raise VaccineManagementException(self.__ERROR_MESSAGE_INVALID_OBJECT)
            super().add_item(item)

    __instance = None

    def __new__(cls):
        if not VaccineJsonStore.__instance:
            VaccineJsonStore.__instance = VaccineJsonStore.__VaccineJsonStore()
        return VaccineJsonStore.__instance
