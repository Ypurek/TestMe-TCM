from enum import Enum


class TestStatus(Enum):
    NORUN = 'NORUN'
    PASS = 'PASS'
    FAIL = 'FAIL'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
