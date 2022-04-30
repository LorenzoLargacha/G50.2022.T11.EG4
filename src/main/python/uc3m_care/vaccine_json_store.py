import json

from .json_store import JsonStore
from .vaccine_log import VaccineLog
from .vaccine_management_exception import VaccineManagementException
from .vaccine_manager_config import JSON_FILES_PATH


class VaccineJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"

    def __init__(self):
        pass

    def add_item(self, vaccine_log: VaccineLog) -> None:
        """Saves the vaccine into a file"""
        if not isinstance(vaccine_log, VaccineLog):
            raise VaccineManagementException("Invalid vaccine log object")
        super().add_item(vaccine_log)
