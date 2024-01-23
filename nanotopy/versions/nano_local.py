import nano_lib_py as nl

# private methods not to use directly


def _get_link_as_hash(link):
    return nl.get_account_public_key(account_id=link) if str(link).startswith("nano_") else link


def _create_block_from_key(private_key, representative, previous, balance, link, work):
    account = get_account_from_key(private_key)
    block = nl.Block(
        block_type="state",
        account=account,
        previous=previous,
        balance=int(str(balance)),
        representative=representative,
        link=_get_link_as_hash(link),
        work=work
    )
    block.sign(private_key)
    return block.json()


# Public methods


def generate_seed():
    return nl.generate_seed()


def get_private_key_from_seed(seed, seed_index):
    return nl.generate_account_private_key(seed, seed_index)


def get_account_from_seed(seed, seed_index):
    return nl.generate_account_id(seed, seed_index)


def get_account_from_key(private_key):
    return nl.get_account_id(private_key=private_key)


def get_account_public_key(account):
    return nl.get_account_public_key(account_id=account)


async def create_send_block_from_key(private_key, frontier, current_balance, amount_to_send, destination, work, representative):
    final_balance = current_balance - amount_to_send
    return _create_block_from_key(private_key, representative, frontier, final_balance, destination, work)


async def create_receive_block_from_key(private_key, frontier, incoming_amount, send_hash, work, representative):
    return _create_block_from_key(private_key, representative, frontier, incoming_amount, send_hash, work)
