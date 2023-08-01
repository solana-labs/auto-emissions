from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class SetProtocolConfigParamsJSON(typing.TypedDict):
    allow_claims: bool
    allow_early_withdrawals: bool
    allow_group_authorities: bool


@dataclass
class SetProtocolConfigParams:
    layout: typing.ClassVar = borsh.CStruct(
        "allow_claims" / borsh.Bool,
        "allow_early_withdrawals" / borsh.Bool,
        "allow_group_authorities" / borsh.Bool,
    )
    allow_claims: bool
    allow_early_withdrawals: bool
    allow_group_authorities: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetProtocolConfigParams":
        return cls(
            allow_claims=obj.allow_claims,
            allow_early_withdrawals=obj.allow_early_withdrawals,
            allow_group_authorities=obj.allow_group_authorities,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "allow_claims": self.allow_claims,
            "allow_early_withdrawals": self.allow_early_withdrawals,
            "allow_group_authorities": self.allow_group_authorities,
        }

    def to_json(self) -> SetProtocolConfigParamsJSON:
        return {
            "allow_claims": self.allow_claims,
            "allow_early_withdrawals": self.allow_early_withdrawals,
            "allow_group_authorities": self.allow_group_authorities,
        }

    @classmethod
    def from_json(cls, obj: SetProtocolConfigParamsJSON) -> "SetProtocolConfigParams":
        return cls(
            allow_claims=obj["allow_claims"],
            allow_early_withdrawals=obj["allow_early_withdrawals"],
            allow_group_authorities=obj["allow_group_authorities"],
        )
