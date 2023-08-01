from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class SetGroupConfigParamsJSON(typing.TypedDict):
    group_authority: str
    allow_claims: bool
    allow_early_withdrawals: bool
    initial_unlock_time: int
    initial_unlock_percent: int
    unlock_frequency: int
    unlock_count: int
    claim_end_time: int


@dataclass
class SetGroupConfigParams:
    layout: typing.ClassVar = borsh.CStruct(
        "group_authority" / BorshPubkey,
        "allow_claims" / borsh.Bool,
        "allow_early_withdrawals" / borsh.Bool,
        "initial_unlock_time" / borsh.U64,
        "initial_unlock_percent" / borsh.U64,
        "unlock_frequency" / borsh.U64,
        "unlock_count" / borsh.U64,
        "claim_end_time" / borsh.U64,
    )
    group_authority: Pubkey
    allow_claims: bool
    allow_early_withdrawals: bool
    initial_unlock_time: int
    initial_unlock_percent: int
    unlock_frequency: int
    unlock_count: int
    claim_end_time: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetGroupConfigParams":
        return cls(
            group_authority=obj.group_authority,
            allow_claims=obj.allow_claims,
            allow_early_withdrawals=obj.allow_early_withdrawals,
            initial_unlock_time=obj.initial_unlock_time,
            initial_unlock_percent=obj.initial_unlock_percent,
            unlock_frequency=obj.unlock_frequency,
            unlock_count=obj.unlock_count,
            claim_end_time=obj.claim_end_time,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "group_authority": self.group_authority,
            "allow_claims": self.allow_claims,
            "allow_early_withdrawals": self.allow_early_withdrawals,
            "initial_unlock_time": self.initial_unlock_time,
            "initial_unlock_percent": self.initial_unlock_percent,
            "unlock_frequency": self.unlock_frequency,
            "unlock_count": self.unlock_count,
            "claim_end_time": self.claim_end_time,
        }

    def to_json(self) -> SetGroupConfigParamsJSON:
        return {
            "group_authority": str(self.group_authority),
            "allow_claims": self.allow_claims,
            "allow_early_withdrawals": self.allow_early_withdrawals,
            "initial_unlock_time": self.initial_unlock_time,
            "initial_unlock_percent": self.initial_unlock_percent,
            "unlock_frequency": self.unlock_frequency,
            "unlock_count": self.unlock_count,
            "claim_end_time": self.claim_end_time,
        }

    @classmethod
    def from_json(cls, obj: SetGroupConfigParamsJSON) -> "SetGroupConfigParams":
        return cls(
            group_authority=Pubkey.from_string(obj["group_authority"]),
            allow_claims=obj["allow_claims"],
            allow_early_withdrawals=obj["allow_early_withdrawals"],
            initial_unlock_time=obj["initial_unlock_time"],
            initial_unlock_percent=obj["initial_unlock_percent"],
            unlock_frequency=obj["unlock_frequency"],
            unlock_count=obj["unlock_count"],
            claim_end_time=obj["claim_end_time"],
        )
