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


class ParticipantJSON(typing.TypedDict):
    group: str
    owner: str
    allocation_percent: int
    claimed_amount: int


@dataclass
class Participant:
    discriminator: typing.ClassVar = b" \x8elO\xf7\xb36\x06"
    layout: typing.ClassVar = borsh.CStruct(
        "group" / BorshPubkey,
        "owner" / BorshPubkey,
        "allocation_percent" / borsh.U64,
        "claimed_amount" / borsh.U64,
    )
    group: Pubkey
    owner: Pubkey
    allocation_percent: int
    claimed_amount: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Participant"]:
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
    ) -> typing.List[typing.Optional["Participant"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Participant"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Participant":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Participant.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            group=dec.group,
            owner=dec.owner,
            allocation_percent=dec.allocation_percent,
            claimed_amount=dec.claimed_amount,
        )

    def to_json(self) -> ParticipantJSON:
        return {
            "group": str(self.group),
            "owner": str(self.owner),
            "allocation_percent": self.allocation_percent,
            "claimed_amount": self.claimed_amount,
        }

    @classmethod
    def from_json(cls, obj: ParticipantJSON) -> "Participant":
        return cls(
            group=Pubkey.from_string(obj["group"]),
            owner=Pubkey.from_string(obj["owner"]),
            allocation_percent=obj["allocation_percent"],
            claimed_amount=obj["claimed_amount"],
        )
