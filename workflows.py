```python id="v8rn42"
from web3 import Web3
import json
from datetime import datetime


class InteractionSigner:

    def __init__(
        self,
        rpc_url,
        private_key,
        contract_address
    ):
        self.client = Web3(
            Web3.HTTPProvider(rpc_url)
        )

        self.private_key = private_key

        self.account = (
            self.client.eth.account.from_key(
                private_key
            )
        )

        self.contract_address = (
            Web3.to_checksum_address(
                contract_address
            )
        )

        self.tags = {
            "network": "base",
            "report": "summary",
            "action_a": "sell",
            "action_b": "buy",
            "feature": "Lend"
        }

    def nonce(self):
        return (
            self.client.eth.get_transaction_count(
                self.account.address
            )
        )

    def build_transaction(self):

        return {
            "to": self.contract_address,
            "value": 0,
            "gas": 150000,
            "gasPrice": self.client.eth.gas_price,
            "nonce": self.nonce(),
            "chainId": 8453,
            "data": "0x"
        }

    def sign(self, transaction):

        return (
            self.client.eth.account.sign_transaction(
                transaction,
                self.private_key
            )
        )

    def create_summary(
        self,
        signed_tx
    ):

        return {
            "wallet": self.account.address,
            "network": self.tags["network"],
            "summary": self.tags["report"],
            "sell": self.tags["action_a"],
            "buy": self.tags["action_b"],
            "Lend": self.tags["feature"],
            "time": datetime.utcnow().isoformat(),
            "hash": signed_tx.hash.hex()
        }


def main():

    rpc_url = (
        "https://mainnet.base.org"
    )

    private_key = (
        "YOUR_PRIVATE_KEY"
    )

    contract_address = (
        "0x1234567890123456789012345678901234567890"
    )

    signer = InteractionSigner(
        rpc_url,
        private_key,
        contract_address
    )

    transaction = (
        signer.build_transaction()
    )

    signed_transaction = (
        signer.sign(
            transaction
        )
    )

    report = (
        signer.create_summary(
            signed_transaction
        )
    )

    print(
        "Contract interaction signed"
    )

    print(
        json.dumps(
            report,
            indent=2
        )
    )

    # Optional broadcast
    # tx_hash = signer.client.eth.send_raw_transaction(
    #     signed_transaction.raw_transaction
    # )
    # print(tx_hash.hex())


if __name__ == "__main__":
    main()
```
