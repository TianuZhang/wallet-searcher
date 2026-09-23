"""A minimal read-only Web3 agent using OpenAI function calling."""

import json
import os

from openai import OpenAI

from wallet_reader import get_eth_balance


TOOLS = [
    {
        "type": "function",
        "name": "get_eth_balance",
        "description": "Read the current native ETH balance of an Ethereum address.",
        "parameters": {
            "type": "object",
            "properties": {
                "wallet_address": {
                    "type": "string",
                    "description": "An Ethereum address beginning with 0x.",
                }
            },
            "required": ["wallet_address"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def run_tool(name: str, arguments: dict) -> str:
    """Execute only the explicitly allowed, read-only Python tools."""
    if name != "get_eth_balance":
        return json.dumps({"error": f"Tool not allowed: {name}"})

    try:
        balance = get_eth_balance(arguments["wallet_address"])
        return json.dumps({"eth_balance": str(balance), "unit": "ETH"})
    except (KeyError, ValueError, ConnectionError) as error:
        return json.dumps({"error": str(error)})


def ask_agent(question: str) -> str:
    """Answer a question by letting the model request approved chain data."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not configured")

    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5"),
        instructions=(
            "You are a Web3 teaching assistant. Use get_eth_balance when a user "
            "asks about an Ethereum address's ETH balance. Explain results in Chinese. "
            "Never claim address ownership, request private keys, or give investment advice."
        ),
        input=question,
        tools=TOOLS,
    )

    for _ in range(3):
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            return response.output_text

        outputs = []
        for call in calls:
            result = run_tool(call.name, json.loads(call.arguments))
            outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": result,
                }
            )

        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5"),
            previous_response_id=response.id,
            input=outputs,
            tools=TOOLS,
        )

    raise RuntimeError("Agent exceeded the maximum number of tool-call rounds")


if __name__ == "__main__":
    user_question = input("Ask about an Ethereum wallet: ").strip()
    print(ask_agent(user_question))
