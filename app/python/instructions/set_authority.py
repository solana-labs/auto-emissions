from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SetAuthorityArgs(typing.TypedDict):
    params: types.set_authority_params.SetAuthorityParams


layout = borsh.CStruct("params" / types.set_authority_params.SetAuthorityParams.layout)


class SetAuthorityAccounts(typing.TypedDict):
    authority: Pubkey
    protocol: Pubkey
    autoemissions_program_data: Pubkey
    autoemissions_program: Pubkey


def set_authority(
    args: SetAuthorityArgs,
    accounts: SetAuthorityAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["protocol"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["autoemissions_program_data"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["autoemissions_program"], is_signer=False, is_writable=False
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x85\xfa%\x15n\xa3\x1ay"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
