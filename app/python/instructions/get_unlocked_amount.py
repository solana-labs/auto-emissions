from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class GetUnlockedAmountArgs(typing.TypedDict):
    params: types.get_unlocked_amount_params.GetUnlockedAmountParams


layout = borsh.CStruct(
    "params" / types.get_unlocked_amount_params.GetUnlockedAmountParams.layout
)


class GetUnlockedAmountAccounts(typing.TypedDict):
    group: Pubkey
    custody: Pubkey


def get_unlocked_amount(
    args: GetUnlockedAmountArgs,
    accounts: GetUnlockedAmountAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["custody"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x16\xb82\xd5<\xa8\xb5\xe3"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
