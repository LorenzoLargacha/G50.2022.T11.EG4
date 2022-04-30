import json

from .json_store import JsonStore
from .vaccine_log import VaccineLog
from .vaccine_management_exception import VaccineManagementException
from .vaccine_manager_config import JSON_FILES_PATH


class VaccineJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"

    def __init__(self):
        pass

    def save_vaccine(self, vaccine_log: VaccineLog) -> None:
        self.add_item(vaccine_log)
