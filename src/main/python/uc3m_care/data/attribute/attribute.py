"""Module attribute"""
import re
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class Attribute:
    """Clase que representa los atributos y sus expresiones regex"""
    def __init__(self):
        self._attr_value = ""
        self._validation_pattern = r""
        self._error_message = ""

    def _validate(self, attr_value: str) -> str:
        """ Método para validar los atributos de un paciente """
        pattern = re.compile(self._validation_pattern)
        result = pattern.fullmatch(attr_value)
        if not result:
            raise VaccineManagementException(self._error_message)
        return attr_value

    @property
    def value(self) -> str:
        """Property that represents the value of an attribute"""
        return self._attr_value

    @value.setter
    def value(self, attr_value: str) -> None:
        self._attr_value = attr_value
