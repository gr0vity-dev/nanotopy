from nanotopy.client_dynamic import NanoRpc
from nanotopy.versions.nano_local import *
from enum import Enum


class ThresholdType(Enum):
    NANO = "nano"  # 1
    RAW = "raw"  # 10^-30 nano


class NanoRpcTyped:
    def __init__(self, auth_key, app_name="nanoto_python_lib", app_email=None):
        self.rpc = NanoRpc(url="https://rpc.nano.to",
                           auth_key=auth_key, app_name=app_name, app_email=app_email)

    async def send(self, private_key, amount_to_send, destination):
        account = get_account_from_key(private_key)
        account_info = await self.account_info(account)
        work = await self.work_generate(account_info["work_hash"])
        frontier = account_info["frontier"]
        current_balance = account_info["balance"]
        representative = account_info["representative"]

        block = await create_send_block_from_key(private_key, frontier, current_balance, amount_to_send, destination, work, representative)
        response = self.process(block)
        return response

    async def receive_block(self, private_key, incoming_amount, send_hash):
        account = get_account_from_key(private_key)
        account_info = await self.account_info(account)
        work_response = await self.work_generate(account_info["work_hash"])
        work = work_response["work"]
        frontier = account_info["frontier"]
        representative = account_info["representative"]
        block = await create_receive_block_from_key(private_key, frontier, incoming_amount, send_hash, work, representative)
        response = await self.process(block)
        return response

    async def receive_blocks_many(self, private_key, threshold=0.000001, threshold_type=ThresholdType.NANO):
        result = []
        account = get_account_from_key(private_key)
        if threshold_type == ThresholdType.NANO:
            threshold_raw = await self.nano_to_raw(threshold)
        else:
            threshold_raw = threshold

        blocks = await self.receivable(account, threshold=threshold_raw, source=True, array=False)
        for block in blocks:
            incoming_amount = block["amount"]
            send_hash = block["hash"]
            response = await self.receive_block(private_key, incoming_amount, send_hash)
            result.append(response)
        return result

    async def version(self):
        return await self.rpc.version()

    async def account_info_from_key(self, private_key):
        account = get_account_from_key(private_key)
        return await self.account_info(account)

    async def account_info(self, account, representative=True, weight=True, receivable=True, include_confirmed=True):
        result: dict
        result = await self.rpc.account_info(account, representative=representative, weight=weight, receivable=receivable, include_confirmed=include_confirmed)
        result.setdefault("work_hash", result.get(
            "frontier", get_account_public_key(account)))
        result.setdefault("frontier", "0"*64)
        result.setdefault("open_block", "0" * 64)
        result.setdefault("block_count", "0")
        result.setdefault("confirmation_height", "0")
        if weight:
            result.setdefault("weight", "0")
        if receivable:
            result.setdefault("receivable_nano", "0")
        if representative:
            result.setdefault("representative", account)

        return result

    async def receivable(self, account, count=None, threshold=None, source=True, include_active=None, min_version=None, sorting=None, include_only_confirmed=True, offset=None, array=False):
        return await self.rpc.receivable(account, count=count, threshold=threshold, source=source, include_active=include_active, min_version=min_version, sorting=sorting, include_only_confirmed=include_only_confirmed, offset=offset, array=array)

    async def account_balance(self, account):
        return await self.rpc.account_balance(account)

    async def account_history(self, account, count=None, raw=None, head=None, offset=None, reverse=None, account_filter=None):
        return await self.rpc.account_history(account, count=count, raw=raw, head=head, offset=offset, reverse=reverse, account_filter=account_filter)

    async def accounts_balances(self, accounts, include_only_confirmed=None):
        return await self.rpc.accounts_balances(accounts, include_only_confirmed=include_only_confirmed)

    async def accounts_receivable(self, accounts, count, threshold=None, source=None, include_active=None, sorting=None, include_only_confirmed=None):
        return await self.rpc.accounts_receivable(accounts, count, threshold=threshold, source=source, include_active=include_active, sorting=sorting, include_only_confirmed=include_only_confirmed)

    async def block_info(self, hash, json_block=None):
        return await self.rpc.block_info(hash, json_block=json_block)

    async def process(self, block, force=None, subtype=None, json_block=False, async_=None):
        return await self.rpc.process(block, force=force, subtype=subtype, json_block=json_block, async_=async_)

    async def work_generate(self, hash):
        return await self.rpc.work_generate(hash)

    async def block_count(self, include_cemented=None):
        return await self.rpc.block_count(include_cemented=include_cemented)

    async def account_key(self, account):
        return await self.rpc.account_key(account)

    async def price(self, currency):
        return await self.rpc.price(currency)

    async def reps(self):
        return await self.rpc.reps()

    async def rep_info(self, account):
        return await self.rpc.rep_info(account)

    async def nano_to_raw(self, amount):
        return await self.rpc.nano_to_raw(amount)

    async def raw_to_nano(self, amount):
        return await self.rpc.raw_to_nano(amount)

    async def known(self):
        return await self.rpc.known()

    async def get_name(self, name):
        return await self.rpc.get_name(name)

    async def update_name(self, name):
        return await self.rpc.update_name(name)

    async def checkout(self, title, notify, webhook):
        return await self.rpc.checkout(title, notify, webhook)

    async def market_data(self):
        return await self.rpc.market_data()

    async def nano_swap(self, amount, from_currency, to, address, refund_address):
        return await self.rpc.nano_swap(amount, from_currency, to, address, refund_address)

    async def nano_ai(self, model, prompt):
        return await self.rpc.nano_ai(model, prompt)

    async def cloud_wallet(self, refund_address, vanity, password):
        return await self.rpc.cloud_wallet(refund_address, vanity, password)

    async def nano_email(self, amount, email_address, refund_address, claimed_webhook, refunded_webhook):
        return await self.rpc.nano_email(amount, email_address, refund_address, claimed_webhook, refunded_webhook)

    async def buy_rpc(self, email):
        return await self.rpc.buy_rpc(email)
