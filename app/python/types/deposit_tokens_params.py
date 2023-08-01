from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class DepositTokensParamsJSON(typing.TypedDict):
    amount: int


@dataclass
class DepositTokensParams:
    layout: typing.ClassVar = borsh.CStruct("amount" / borsh.U64)
    amount: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "DepositTokensParams":
        return cls(amount=obj.amount)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"amount": self.amount}

    def to_json(self) -> DepositTokensParamsJSON:
        return {"amount": self.amount}

    @classmethod
    def from_json(cls, obj: DepositTokensParamsJSON) -> "DepositTokensParams":
        return cls(amount=obj["amount"])
