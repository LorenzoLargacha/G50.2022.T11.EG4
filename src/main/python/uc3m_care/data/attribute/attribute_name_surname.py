"""Module attribute_name_surname"""
from uc3m_care.data.attribute.attribute import Attribute


class NameSurname(Attribute):
    """Clase hija de attribute para la validación del nombre"""
    def __init__(self, attr_value: str) -> None:
        super().__init__()
        self._validation_pattern = r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$"
        self._error_message = "name surname is not valid"
        self._attr_value = self._validate(attr_value)
