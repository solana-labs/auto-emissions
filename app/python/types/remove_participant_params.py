from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class RemoveParticipantParamsJSON(typing.TypedDict):
    pass


@dataclass
class RemoveParticipantParams:
    layout: typing.ClassVar = borsh.CStruct()

    @classmethod
    def from_decoded(cls, obj: Container) -> "RemoveParticipantParams":
        return cls()

    def to_encodable(self) -> dict[str, typing.Any]:
        return {}

    def to_json(self) -> RemoveParticipantParamsJSON:
        return {}

    @classmethod
    def from_json(cls, obj: RemoveParticipantParamsJSON) -> "RemoveParticipantParams":
        return cls()
