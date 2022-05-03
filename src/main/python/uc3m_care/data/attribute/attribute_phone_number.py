"""Module attribute_phone_number"""
from uc3m_care.data.attribute.attribute import Attribute


class PhoneNumber(Attribute):
    """Clase hija de attribute para la validacion del telefono"""
    def __init__(self, attr_value: str) -> None:
        super().__init__()
        self._validation_pattern = r"^(\+)[0-9]{11}"
        self._error_message = "phone number is not valid"
        self._attr_value = self._validate(attr_value)
