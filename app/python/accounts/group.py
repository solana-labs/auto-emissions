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


class GroupJSON(typing.TypedDict):
    project_name: str
    group_name: str
    group_authority: str
    allow_claims: bool
    allow_early_withdrawals: bool
    initial_unlock_time: int
    initial_unlock_percent: int
    unlock_frequency: int
    unlock_count: int
    claim_end_time: int
    custody: str
    mint: str
    mint_decimals: int
    claimed_amount: int
    participants: int
    allocation_percent: int
    inception_time: int


@dataclass
class Group:
    discriminator: typing.ClassVar = b"\xd1\xf9\xd0?\xb6Y\xba\xfe"
    layout: typing.ClassVar = borsh.CStruct(
        "project_name" / borsh.String,
        "group_name" / borsh.String,
        "group_authority" / BorshPubkey,
        "allow_claims" / borsh.Bool,
        "allow_early_withdrawals" / borsh.Bool,
        "initial_unlock_time" / borsh.U64,
        "initial_unlock_percent" / borsh.U64,
        "unlock_frequency" / borsh.U64,
        "unlock_count" / borsh.U64,
        "claim_end_time" / borsh.U64,
        "custody" / BorshPubkey,
        "mint" / BorshPubkey,
        "mint_decimals" / borsh.U8,
        "claimed_amount" / borsh.U64,
        "participants" / borsh.U64,
        "allocation_percent" / borsh.U64,
        "inception_time" / borsh.U64,
    )
    project_name: str
    group_name: str
    group_authority: Pubkey
    allow_claims: bool
    allow_early_withdrawals: bool
    initial_unlock_time: int
    initial_unlock_percent: int
    unlock_frequency: int
    unlock_count: int
    claim_end_time: int
    custody: Pubkey
    mint: Pubkey
    mint_decimals: int
    claimed_amount: int
    participants: int
    allocation_percent: int
    inception_time: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Group"]:
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
    ) -> typing.List[typing.Optional["Group"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Group"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Group":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Group.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            project_name=dec.project_name,
            group_name=dec.group_name,
            group_authority=dec.group_authority,
            allow_claims=dec.allow_claims,
            allow_early_withdrawals=dec.allow_early_withdrawals,
            initial_unlock_time=dec.initial_unlock_time,
            initial_unlock_percent=dec.initial_unlock_percent,
            unlock_frequency=dec.unlock_frequency,
            unlock_count=dec.unlock_count,
            claim_end_time=dec.claim_end_time,
            custody=dec.custody,
            mint=dec.mint,
            mint_decimals=dec.mint_decimals,
            claimed_amount=dec.claimed_amount,
            participants=dec.participants,
            allocation_percent=dec.allocation_percent,
            inception_time=dec.inception_time,
        )

    def to_json(self) -> GroupJSON:
        return {
            "project_name": self.project_name,
            "group_name": self.group_name,
            "group_authority": str(self.group_authority),
            "allow_claims": self.allow_claims,
            "allow_early_withdrawals": self.allow_early_withdrawals,
            "initial_unlock_time": self.initial_unlock_time,
            "initial_unlock_percent": self.initial_unlock_percent,
            "unlock_frequency": self.unlock_frequency,
            "unlock_count": self.unlock_count,
            "claim_end_time": self.claim_end_time,
            "custody": str(self.custody),
            "mint": str(self.mint),
            "mint_decimals": self.mint_decimals,
            "claimed_amount": self.claimed_amount,
            "participants": self.participants,
            "allocation_percent": self.allocation_percent,
            "inception_time": self.inception_time,
        }

    @classmethod
    def from_json(cls, obj: GroupJSON) -> "Group":
        return cls(
            project_name=obj["project_name"],
            group_name=obj["group_name"],
            group_authority=Pubkey.from_string(obj["group_authority"]),
            allow_claims=obj["allow_claims"],
            allow_early_withdrawals=obj["allow_early_withdrawals"],
            initial_unlock_time=obj["initial_unlock_time"],
            initial_unlock_percent=obj["initial_unlock_percent"],
            unlock_frequency=obj["unlock_frequency"],
            unlock_count=obj["unlock_count"],
            claim_end_time=obj["claim_end_time"],
            custody=Pubkey.from_string(obj["custody"]),
            mint=Pubkey.from_string(obj["mint"]),
            mint_decimals=obj["mint_decimals"],
            claimed_amount=obj["claimed_amount"],
            participants=obj["participants"],
            allocation_percent=obj["allocation_percent"],
            inception_time=obj["inception_time"],
        )
