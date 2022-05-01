from uc3m_care.data.attribute.attribute import Attribute


class RegistrationType(Attribute):
    def __init__(self, attr_value: str) -> None:
        self._validation_pattern = r"(Regular|Family)"
        self._error_message = "Registration type is nor valid"
        self._attr_value = self._validate(attr_value)
