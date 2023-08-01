from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class GetEntitledAmountArgs(typing.TypedDict):
    params: types.get_entitled_amount_params.GetEntitledAmountParams


layout = borsh.CStruct(
    "params" / types.get_entitled_amount_params.GetEntitledAmountParams.layout
)


class GetEntitledAmountAccounts(typing.TypedDict):
    group: Pubkey
    custody: Pubkey
    participant: Pubkey


def get_entitled_amount(
    args: GetEntitledAmountArgs,
    accounts: GetEntitledAmountAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["custody"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["participant"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe8&\xe7\xd14\xc6\x88\x97"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
