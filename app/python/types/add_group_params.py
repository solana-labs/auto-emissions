from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class AddGroupParamsJSON(typing.TypedDict):
    project_name: str
    group_name: str
    group_authority: str
    allow_claims: bool
    allow_early_withdrawals: bool
    initial_unlock_time: int
    initial_unlock_percent: int
    unlock_frequency: int
    unlock_count: int
    claim_end_time: int


@dataclass
class AddGroupParams:
    layout: typing.ClassVar = borsh.CStruct(
        "project_name" / borsh.String,
        "group_name" / borsh.String,
        "group_authority" / BorshPubkey,
        "allow_claims" / borsh.Bool,
        "allow_early_withdrawals" / borsh.Bool,
        "initial_unlock_time" / borsh.U64,
        "initial_unlock_percent" / borsh.U64,
        "unlock_frequency" / borsh.U64,
        "unlock_count" / borsh.U64,
        "claim_end_time" / borsh.U64,
    )
    project_name: str
    group_name: str
    group_authority: Pubkey
    allow_claims: bool
    allow_early_withdrawals: bool
    initial_unlock_time: int
    initial_unlock_percent: int
    unlock_frequency: int
    unlock_count: int
    claim_end_time: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "AddGroupParams":
        return cls(
            project_name=obj.project_name,
            group_name=obj.group_name,
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
            "project_name": self.project_name,
            "group_name": self.group_name,
            "group_authority": self.group_authority,
            "allow_claims": self.allow_claims,
            "allow_early_withdrawals": self.allow_early_withdrawals,
            "initial_unlock_time": self.initial_unlock_time,
            "initial_unlock_percent": self.initial_unlock_percent,
            "unlock_frequency": self.unlock_frequency,
            "unlock_count": self.unlock_count,
            "claim_end_time": self.claim_end_time,
        }

    def to_json(self) -> AddGroupParamsJSON:
        return {
            "project_name": self.project_name,
            "group_name": self.group_name,
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
    def from_json(cls, obj: AddGroupParamsJSON) -> "AddGroupParams":
        return cls(
            project_name=obj["project_name"],
            group_name=obj["group_name"],
            group_authority=Pubkey.from_string(obj["group_authority"]),
            allow_claims=obj["allow_claims"],
            allow_early_withdrawals=obj["allow_early_withdrawals"],
            initial_unlock_time=obj["initial_unlock_time"],
            initial_unlock_percent=obj["initial_unlock_percent"],
            unlock_frequency=obj["unlock_frequency"],
            unlock_count=obj["unlock_count"],
            claim_end_time=obj["claim_end_time"],
        )
