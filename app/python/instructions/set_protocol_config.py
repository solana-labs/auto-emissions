from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SetProtocolConfigArgs(typing.TypedDict):
    params: types.set_protocol_config_params.SetProtocolConfigParams


layout = borsh.CStruct(
    "params" / types.set_protocol_config_params.SetProtocolConfigParams.layout
)


class SetProtocolConfigAccounts(typing.TypedDict):
    authority: Pubkey
    protocol: Pubkey


def set_protocol_config(
    args: SetProtocolConfigArgs,
    accounts: SetProtocolConfigAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["protocol"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xcb\xba\xda\xe1\x8e\x1b\x18l"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
