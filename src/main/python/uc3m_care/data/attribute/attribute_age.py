"""Module attribute_age"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class Age(Attribute):
    """Clase hija de attribute para la validación de la edad"""
    def __init__(self, attr_value: str) -> None:
        super().__init__()
        self._error_message = "age is not valid"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value: str) -> str:
        """ Método para sobreescribir _validate de la clase Attribute """
        if attr_value.isnumeric():
            if int(attr_value) < 6 or int(attr_value) > 125:
                raise VaccineManagementException(self._error_message)
        else:
            raise VaccineManagementException(self._error_message)
        return attr_value
