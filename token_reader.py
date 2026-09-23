"""Read ERC-20 token balances from the Ethereum mainnet."""

import os
from decimal import Decimal

from web3 import Web3


# The smallest ABI needed to read standard ERC-20 metadata and balances.
ERC20_READ_ABI = [
    {
        "type": "function",
        "name": "balanceOf",
        "inputs": [{"name": "owner", "type": "address"}],
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "decimals",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "symbol",
        "inputs": [],
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
    },
]


def get_token_balance(wallet_address: str, token_address: str) -> dict[str, str]:
    """Return a standard ERC-20 token's symbol and human-readable balance."""
    rpc_url = os.getenv("ETH_RPC_URL")
    if not rpc_url:
        raise ValueError("ETH_RPC_URL is not configured")

    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Could not connect to the Ethereum RPC endpoint")
    if not web3.is_address(wallet_address) or not web3.is_address(token_address):
        raise ValueError("Wallet address or token contract address is invalid")

    token = web3.eth.contract(
        address=web3.to_checksum_address(token_address),
        abi=ERC20_READ_ABI,
    )
    raw_balance = token.functions.balanceOf(
        web3.to_checksum_address(wallet_address)
    ).call()
    decimals = token.functions.decimals().call()
    symbol = token.functions.symbol().call()

    balance = Decimal(raw_balance) / Decimal(10**decimals)
    return {"symbol": symbol, "balance": str(balance)}


if __name__ == "__main__":
    wallet = input("Ethereum wallet address: ").strip()
    token_contract = input("ERC-20 token contract address: ").strip()
    result = get_token_balance(wallet, token_contract)
    print(f"{result['symbol']} balance: {result['balance']}")
