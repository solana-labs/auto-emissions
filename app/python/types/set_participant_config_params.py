from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class SetParticipantConfigParamsJSON(typing.TypedDict):
    owner: str
    allocation_percent: int


@dataclass
class SetParticipantConfigParams:
    layout: typing.ClassVar = borsh.CStruct(
        "owner" / BorshPubkey, "allocation_percent" / borsh.U64
    )
    owner: Pubkey
    allocation_percent: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetParticipantConfigParams":
        return cls(owner=obj.owner, allocation_percent=obj.allocation_percent)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"owner": self.owner, "allocation_percent": self.allocation_percent}

    def to_json(self) -> SetParticipantConfigParamsJSON:
        return {"owner": str(self.owner), "allocation_percent": self.allocation_percent}

    @classmethod
    def from_json(
        cls, obj: SetParticipantConfigParamsJSON
    ) -> "SetParticipantConfigParams":
        return cls(
            owner=Pubkey.from_string(obj["owner"]),
            allocation_percent=obj["allocation_percent"],
        )
