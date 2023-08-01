from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class RemoveParticipantArgs(typing.TypedDict):
    params: types.remove_participant_params.RemoveParticipantParams


layout = borsh.CStruct(
    "params" / types.remove_participant_params.RemoveParticipantParams.layout
)


class RemoveParticipantAccounts(typing.TypedDict):
    authority: Pubkey
    protocol: Pubkey
    group: Pubkey
    participant: Pubkey


def remove_participant(
    args: RemoveParticipantArgs,
    accounts: RemoveParticipantAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["protocol"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["participant"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"&\x96t\x7f\xfc\x19\x86w"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
