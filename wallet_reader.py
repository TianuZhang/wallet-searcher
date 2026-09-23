"""Read the native ETH balance of an Ethereum address."""

import os
from decimal import Decimal

from web3 import Web3


def get_eth_balance(address: str, rpc_url: str | None = None) -> Decimal:
    """Return an address's ETH balance as a Decimal."""
    rpc_url = rpc_url or os.getenv("ETH_RPC_URL")
    if not rpc_url:
        raise ValueError("ETH_RPC_URL is not configured")

    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Could not connect to the Ethereum RPC endpoint")
    if not web3.is_address(address):
        raise ValueError(f"Invalid Ethereum address: {address}")

    checksum_address = web3.to_checksum_address(address)
    balance_wei = web3.eth.get_balance(checksum_address)
    return Decimal(balance_wei) / Decimal(10**18)


if __name__ == "__main__":
    wallet_address = input("Ethereum wallet address: ").strip()
    balance = get_eth_balance(wallet_address)
    print(f"ETH balance: {balance}")
