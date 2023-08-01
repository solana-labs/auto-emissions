from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class RemoveGroupArgs(typing.TypedDict):
    params: types.remove_group_params.RemoveGroupParams


layout = borsh.CStruct("params" / types.remove_group_params.RemoveGroupParams.layout)


class RemoveGroupAccounts(typing.TypedDict):
    authority: Pubkey
    protocol: Pubkey
    transfer_authority: Pubkey
    group: Pubkey
    custody: Pubkey


def remove_group(
    args: RemoveGroupArgs,
    accounts: RemoveGroupAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["protocol"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["transfer_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["custody"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xd0\x054\xc3\xa90\x1f="
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
