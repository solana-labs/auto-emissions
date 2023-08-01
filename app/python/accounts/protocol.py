import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID


class ProtocolJSON(typing.TypedDict):
    authority: str
    allow_claims: bool
    allow_early_withdrawals: bool
    allow_group_authorities: bool
    transfer_authority_bump: int


@dataclass
class Protocol:
    discriminator: typing.ClassVar = b"-'e+sH\x83("
    layout: typing.ClassVar = borsh.CStruct(
        "authority" / BorshPubkey,
        "allow_claims" / borsh.Bool,
        "allow_early_withdrawals" / borsh.Bool,
        "allow_group_authorities" / borsh.Bool,
        "transfer_authority_bump" / borsh.U8,
    )
    authority: Pubkey
    allow_claims: bool
    allow_early_withdrawals: bool
    allow_group_authorities: bool
    transfer_authority_bump: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Protocol"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["Protocol"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Protocol"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Protocol":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Protocol.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            authority=dec.authority,
            allow_claims=dec.allow_claims,
            allow_early_withdrawals=dec.allow_early_withdrawals,
            allow_group_authorities=dec.allow_group_authorities,
            transfer_authority_bump=dec.transfer_authority_bump,
        )

    def to_json(self) -> ProtocolJSON:
        return {
            "authority": str(self.authority),
            "allow_claims": self.allow_claims,
            "allow_early_withdrawals": self.allow_early_withdrawals,
            "allow_group_authorities": self.allow_group_authorities,
            "transfer_authority_bump": self.transfer_authority_bump,
        }

    @classmethod
    def from_json(cls, obj: ProtocolJSON) -> "Protocol":
        return cls(
            authority=Pubkey.from_string(obj["authority"]),
            allow_claims=obj["allow_claims"],
            allow_early_withdrawals=obj["allow_early_withdrawals"],
            allow_group_authorities=obj["allow_group_authorities"],
            transfer_authority_bump=obj["transfer_authority_bump"],
        )
