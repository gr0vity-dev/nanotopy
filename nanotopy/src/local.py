import nano_lib_py as nl


class NanoLocalHandler:
    def __init__(self, seed_index=0):
        self.seed = nl.generate_seed()
        self.private_key = nl.generate_account_private_key(
            self.seed, seed_index)
        self.bot_account_address = nl.generate_account_id(
            self.seed, seed_index)

    def get_account_public_key(self, account_id):
        return nl.get_account_public_key(account_id=account_id)

    def get_link_as_hash(self, link):
        return nl.get_account_public_key(account_id=link) if str(link).startswith("nano_") else link

    def create_block(self, block_type, account, representative, previous, balance, link, work):
        block = nl.Block(
            block_type=block_type,
            account=account,
            representative=representative,
            previous=previous,
            balance=balance,
            link=self.get_link_as_hash(link),
            work=work
        )
        block.sign(self.private_key)
        return block
