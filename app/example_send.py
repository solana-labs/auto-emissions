from solana.transaction import Transaction
from solana.rpc.core import RPCException
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from anchorpy import Provider
from python.errors import from_tx_error
from python.instructions import init
from python.types import InitParams
from python.program_id import PROGRAM_ID


async def main():
    provider = Provider.local(url="http://localhost:8899")
    recent_blockhash = (await provider.connection.get_latest_blockhash()).value

    params = InitParams(
        authority=provider.wallet.public_key,
        allow_claims=True,
        allow_early_withdrawals=True,
        allow_group_authorities=True,
    )

    [protocol, bump] = Pubkey.find_program_address([b"protocol"], PROGRAM_ID)

    [transfer_authority,
     bump] = Pubkey.find_program_address([b"transfer_authority"], PROGRAM_ID)

    [program_data, bump] = Pubkey.find_program_address(
        [bytes(PROGRAM_ID)],
        Pubkey.from_string("BPFLoaderUpgradeab1e11111111111111111111111"))

    ix = init({"params": params}, {
        "upgrade_authority": provider.wallet.public_key,
        "protocol": protocol,
        "transfer_authority": transfer_authority,
        "autoemissions_program_data": program_data,
        "autoemissions_program": PROGRAM_ID,
    })
    tx = Transaction(recent_blockhash.blockhash).add(ix)
    provider.wallet.sign_transaction(tx)

    try:
        await provider.send(tx)
    except RPCException as exc:
        parsed = from_tx_error(exc)
        if parsed:
            raise parsed from exc
        else:
            raise exc


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())