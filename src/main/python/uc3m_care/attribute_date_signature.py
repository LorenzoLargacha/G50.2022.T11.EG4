from .attribute import Attribute

class DateSignature(Attribute):
    def __init__(self, attr_value: str) -> None:
        self._validation_pattern = r"[0-9a-fA-F]{64}$"
        self._error_message = "date_signature format is not valid"
        self._attr_value = self._validate(attr_value)
