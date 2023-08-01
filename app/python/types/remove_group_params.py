from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class RemoveGroupParamsJSON(typing.TypedDict):
    pass


@dataclass
class RemoveGroupParams:
    layout: typing.ClassVar = borsh.CStruct()

    @classmethod
    def from_decoded(cls, obj: Container) -> "RemoveGroupParams":
        return cls()

    def to_encodable(self) -> dict[str, typing.Any]:
        return {}

    def to_json(self) -> RemoveGroupParamsJSON:
        return {}

    @classmethod
    def from_json(cls, obj: RemoveGroupParamsJSON) -> "RemoveGroupParams":
        return cls()
