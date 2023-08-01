from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class InitParamsJSON(typing.TypedDict):
    authority: str
    allow_claims: bool
    allow_early_withdrawals: bool
    allow_group_authorities: bool


@dataclass
class InitParams:
    layout: typing.ClassVar = borsh.CStruct(
        "authority" / BorshPubkey,
        "allow_claims" / borsh.Bool,
        "allow_early_withdrawals" / borsh.Bool,
        "allow_group_authorities" / borsh.Bool,
    )
    authority: Pubkey
    allow_claims: bool
    allow_early_withdrawals: bool
    allow_group_authorities: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitParams":
        return cls(
            authority=obj.authority,
            allow_claims=obj.allow_claims,
            allow_early_withdrawals=obj.allow_early_withdrawals,
            allow_group_authorities=obj.allow_group_authorities,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "authority": self.authority,
            "allow_claims": self.allow_claims,
            "allow_early_withdrawals": self.allow_early_withdrawals,
            "allow_group_authorities": self.allow_group_authorities,
        }

    def to_json(self) -> InitParamsJSON:
        return {
            "authority": str(self.authority),
            "allow_claims": self.allow_claims,
            "allow_early_withdrawals": self.allow_early_withdrawals,
            "allow_group_authorities": self.allow_group_authorities,
        }

    @classmethod
    def from_json(cls, obj: InitParamsJSON) -> "InitParams":
        return cls(
            authority=Pubkey.from_string(obj["authority"]),
            allow_claims=obj["allow_claims"],
            allow_early_withdrawals=obj["allow_early_withdrawals"],
            allow_group_authorities=obj["allow_group_authorities"],
        )
