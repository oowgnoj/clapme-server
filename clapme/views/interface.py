from dataclasses import dataclass


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


# request schemas
routine_post_request = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'alarm': {'type': 'boolean'},
        'time': {'type': 'string'},
        'mon': {'type': 'boolean'},
        'tue': {'type': 'boolean'},
        'wed': {'type': 'boolean'},
        'thu': {'type': 'boolean'},
        'fri': {'type': 'boolean'},
        'sat': {'type': 'boolean'},
        'sun': {'type': 'boolean'},
        'color': {'type': 'string'},
        'description': {'type': 'string'},
    },
    'required': [
        'title',
        'alarm',
        'time',
        'mon',
        'tue',
        'wed',
        'thu',
        'fri',
        'sat',
        'sun',
        'color'
    ]
}
