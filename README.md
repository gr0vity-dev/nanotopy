
### nanoto_py : Python gateway to rpc.nano.to
The goal is to create the easiest way to prototype nano apps.

Get your free API_KEY from https://rpc.nano.to and hack around!

### How to install :
``` 
pip install nanotopy
```
or from source :
```
git clone https://github.com/gr0vity-dev/nanotopy.git
cd nanotopy
pip install .
```



### Example code :
```python
import asyncio
from nanotopy.client import NanoTo

async def run():

    # This can only be done once ! Write down the key!
    AUTH_KEY = await NanoTo.get_auth_key("your@email.address")
    print(AUTH_KEY)
    nano_to = NanoTo(AUTH_KEY["key"])

    # Create a new nano account
    # Seed generation is done locally! No secrets are ever shared
    seed = NanoTo.generate_seed()
    seed_index = 0
    # Same seed and seed_index will ALWAYS result in the same private_key
    private_key = NanoTo.get_private_key_from_seed(seed, seed_index)
    account = NanoTo.get_account_from_key(private_key)
    print(account)

    # Get account info
    account_info = await nano_to.account_info(account)
    print(account_info)

    # Receive all blocks
    received_hashes = await nano_to.receive_blocks_many(private_key)
    print(received_hashes)


if __name__ == "__main__":
    asyncio.run(run())
```
