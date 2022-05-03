"""Module attribute_date_signature"""
from uc3m_care.data.attribute.attribute import Attribute


class DateSignature(Attribute):
    """Clase hija de attribute para la validación del date_signature"""
    def __init__(self, attr_value: str) -> None:
        super().__init__()
        self._validation_pattern = r"[0-9a-fA-F]{64}$"
        self._error_message = "date_signature format is not valid"
        self._attr_value = self._validate(attr_value)
