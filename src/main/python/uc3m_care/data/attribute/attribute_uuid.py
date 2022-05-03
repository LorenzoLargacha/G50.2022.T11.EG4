"""Module attribute_uuid"""
import uuid
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class Uuid(Attribute):
    """Clase hija de attribute para la validacion del uuid"""
    def __init__(self, attr_value: str) -> None:
        super().__init__()
        self._validation_pattern = r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]" \
                                   r"{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
        self._error_message = "UUID invalid"
        self.__uuid_error_message = "Id received is not a UUID"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value: str) -> str:
        """ Método para sobreescribir _validate de la clase Attribute """
        try:
            uuid.UUID(attr_value)
            # Llamamos al _validate de la clase abstracta
            super()._validate(attr_value)
        except ValueError as val_er:
            raise VaccineManagementException(self.__uuid_error_message) from val_er
        return attr_value
