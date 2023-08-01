from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class GetUnlockedAmountParamsJSON(typing.TypedDict):
    time: int


@dataclass
class GetUnlockedAmountParams:
    layout: typing.ClassVar = borsh.CStruct("time" / borsh.U64)
    time: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "GetUnlockedAmountParams":
        return cls(time=obj.time)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"time": self.time}

    def to_json(self) -> GetUnlockedAmountParamsJSON:
        return {"time": self.time}

    @classmethod
    def from_json(cls, obj: GetUnlockedAmountParamsJSON) -> "GetUnlockedAmountParams":
        return cls(time=obj["time"])
