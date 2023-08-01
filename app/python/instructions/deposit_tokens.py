from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class DepositTokensArgs(typing.TypedDict):
    params: types.deposit_tokens_params.DepositTokensParams


layout = borsh.CStruct(
    "params" / types.deposit_tokens_params.DepositTokensParams.layout
)


class DepositTokensAccounts(typing.TypedDict):
    owner: Pubkey
    funding_account: Pubkey
    group: Pubkey
    custody: Pubkey


def deposit_tokens(
    args: DepositTokensArgs,
    accounts: DepositTokensAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["funding_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["custody"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xb0S\xe5\x12\xbf\x8f\xb0\x96"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
