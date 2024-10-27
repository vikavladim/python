from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShipClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Corvette: _ClassVar[ShipClass]
    Frigate: _ClassVar[ShipClass]
    Cruiser: _ClassVar[ShipClass]
    Destroyer: _ClassVar[ShipClass]
    Carrier: _ClassVar[ShipClass]
    Dreadnought: _ClassVar[ShipClass]

class Alignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Ally: _ClassVar[Alignment]
    Enemy: _ClassVar[Alignment]
Corvette: ShipClass
Frigate: ShipClass
Cruiser: ShipClass
Destroyer: ShipClass
Carrier: ShipClass
Dreadnought: ShipClass
Ally: Alignment
Enemy: Alignment

class Officer(_message.Message):
    __slots__ = ("first_name", "last_name", "rank")
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    rank: str
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., rank: _Optional[str] = ...) -> None: ...

class ShipResponse(_message.Message):
    __slots__ = ("alignment", "ship_class", "name", "length", "crew_size", "is_armed", "officers")
    ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    SHIP_CLASS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    CREW_SIZE_FIELD_NUMBER: _ClassVar[int]
    IS_ARMED_FIELD_NUMBER: _ClassVar[int]
    OFFICERS_FIELD_NUMBER: _ClassVar[int]
    alignment: Alignment
    ship_class: ShipClass
    name: str
    length: float
    crew_size: int
    is_armed: bool
    officers: _containers.RepeatedCompositeFieldContainer[Officer]
    def __init__(self, alignment: _Optional[_Union[Alignment, str]] = ..., ship_class: _Optional[_Union[ShipClass, str]] = ..., name: _Optional[str] = ..., length: _Optional[float] = ..., crew_size: _Optional[int] = ..., is_armed: bool = ..., officers: _Optional[_Iterable[_Union[Officer, _Mapping]]] = ...) -> None: ...

class RigthAscention(_message.Message):
    __slots__ = ("hours", "minutes", "seconds")
    HOURS_FIELD_NUMBER: _ClassVar[int]
    MINUTES_FIELD_NUMBER: _ClassVar[int]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    hours: float
    minutes: float
    seconds: float
    def __init__(self, hours: _Optional[float] = ..., minutes: _Optional[float] = ..., seconds: _Optional[float] = ...) -> None: ...

class Declination(_message.Message):
    __slots__ = ("degrees", "minutes", "seconds")
    DEGREES_FIELD_NUMBER: _ClassVar[int]
    MINUTES_FIELD_NUMBER: _ClassVar[int]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    degrees: float
    minutes: float
    seconds: float
    def __init__(self, degrees: _Optional[float] = ..., minutes: _Optional[float] = ..., seconds: _Optional[float] = ...) -> None: ...

class Coordinates(_message.Message):
    __slots__ = ("right_ascention", "declination")
    RIGHT_ASCENTION_FIELD_NUMBER: _ClassVar[int]
    DECLINATION_FIELD_NUMBER: _ClassVar[int]
    right_ascention: RigthAscention
    declination: Declination
    def __init__(self, right_ascention: _Optional[_Union[RigthAscention, _Mapping]] = ..., declination: _Optional[_Union[Declination, _Mapping]] = ...) -> None: ...

class ShipResponseList(_message.Message):
    __slots__ = ("responses",)
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.RepeatedCompositeFieldContainer[ShipResponse]
    def __init__(self, responses: _Optional[_Iterable[_Union[ShipResponse, _Mapping]]] = ...) -> None: ...
