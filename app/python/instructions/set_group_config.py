from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SetGroupConfigArgs(typing.TypedDict):
    params: types.set_group_config_params.SetGroupConfigParams


layout = borsh.CStruct(
    "params" / types.set_group_config_params.SetGroupConfigParams.layout
)


class SetGroupConfigAccounts(typing.TypedDict):
    authority: Pubkey
    protocol: Pubkey
    group: Pubkey


def set_group_config(
    args: SetGroupConfigArgs,
    accounts: SetGroupConfigAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["protocol"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["group"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xb0\xbcY\xbe\xc6\x8f\x1a\xa2"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
