class CommonException(Exception):
    """Excepción base para errores comunes del proyecto."""


class BusinessRuleException(CommonException):
    """Error cuando una regla de negocio no se cumple."""


class InvalidActionException(CommonException):
    """Error cuando una acción no está permitida."""