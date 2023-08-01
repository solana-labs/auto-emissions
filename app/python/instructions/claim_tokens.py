from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ClaimTokensArgs(typing.TypedDict):
    params: types.claim_tokens_params.ClaimTokensParams


layout = borsh.CStruct("params" / types.claim_tokens_params.ClaimTokensParams.layout)


class ClaimTokensAccounts(typing.TypedDict):
    owner: Pubkey
    receiving_account: Pubkey
    protocol: Pubkey
    transfer_authority: Pubkey
    group: Pubkey
    custody: Pubkey
    participant: Pubkey


def claim_tokens(
    args: ClaimTokensArgs,
    accounts: ClaimTokensAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["receiving_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["protocol"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["transfer_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["custody"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["participant"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"l\xd8\xd2\xe7\x00\xd4*@"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
