from enum import StrEnum, auto

__all__ = ('UserRole',)


class UserRole(StrEnum):
    CLIENT = auto()
    ADMIN = auto()
    SALESMAN = auto()
