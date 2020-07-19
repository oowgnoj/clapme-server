from dataclasses import dataclass
from enum import Enum
from typing import List


class Days(Enum):
    mon = 'mon'
    tue = 'tue'
    wed = 'wed'
    thu = 'thu'
    fri = 'fri'
    sat = 'sat'
    sun = 'sun'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


@dataclass
class RoutineDto:
    id: str
    title: str
    alarm: bool
    time: str
    mon: bool
    tue: bool
    wed: bool
    thu: bool
    fri: bool
    sat: bool
    sun: bool
    color: str
    description: str = None


@dataclass
class RoutineStatusDto:
    id: str
    title: str
    alarm: bool
    time: str
    color: str
    success: bool


@dataclass
class ColorDto:
    main: str
    sub: str


@dataclass
class RoutineSampleDto:
    time: str
    title: str


@dataclass
class IdeaDto:
    title: str
    subTitle: str
    contents: str
    picUrl: str
    routines: List[RoutineSampleDto]


@dataclass
class ScheduleDto:
    mon: bool = False
    tue: bool = False
    wed: bool = False
    thu: bool = False
    fri: bool = False
    sat: bool = False
    sun: bool = False

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, key):
        return getattr(self, key)


