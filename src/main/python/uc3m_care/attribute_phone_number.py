from .attribute import Attribute

class PhoneNumber(Attribute):
    def __init__(self, attr_value: str) -> None:
        self._validation_pattern = r"^(\+)[0-9]{11}"
        self._error_message = "phone number is not valid"
        self._attr_value = self._validate(attr_value)
