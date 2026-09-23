"""Read an ETH balance and ask OpenAI to explain it."""

import os

from openai import OpenAI

from wallet_reader import get_eth_balance


def explain_eth_balance(wallet_address: str) -> str:
    balance = get_eth_balance(wallet_address)

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not configured")

    client = OpenAI()
    response = client.responses.create(
        model="gpt-5",
        input=(
            "你是一个 Web3 教学助手。"
            f"钱包地址 {wallet_address} 当前有 {balance} ETH。"
            "请用初学者能理解的中文解释这代表什么，"
            "不要假设这个钱包属于用户，也不要提供投资建议。"
        ),
    )
    return response.output_text


if __name__ == "__main__":
    address = input("Ethereum wallet address: ").strip()
    print(explain_eth_balance(address))
