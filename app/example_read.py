from anchorpy import Provider
from solders.pubkey import Pubkey
from python.accounts import Protocol
from python.program_id import PROGRAM_ID
from json import dumps


async def main():
    provider = Provider.local(url="http://localhost:8899")

    [protocol, bump] = Pubkey.find_program_address([b"protocol"], PROGRAM_ID)

    data = await Protocol.fetch(provider.connection, protocol)
    if data is None:
        raise ValueError("account not found")

    obj = data.to_json()
    print(dumps(obj, indent=2))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())