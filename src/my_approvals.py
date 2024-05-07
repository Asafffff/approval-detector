import argparse
from web3 import Web3
from constant import BYTES_INFINITE
from os import environ
from dotenv import load_dotenv

load_dotenv()


def get_w3_instance() -> Web3:
    w3 = Web3(
        Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{environ['INFURA_API_KEY']}")
    )

    if not w3.is_connected():
        raise ConnectionResetError("Failed to connect to Ethereum network!")

    return w3


def build_get_logs_filter_params(w3: Web3, address: str) -> dict:
    # Define the ERC-20 token Approval event signature
    approval_signature_hash = w3.keccak(text="Approval(address,address,uint256)").hex()
    padded_address = "0x" + Web3.to_checksum_address(address)[2:].rjust(64, "0")

    filter_params = {
        "fromBlock": "earliest",
        "toBlock": "latest",
        "topics": [approval_signature_hash, padded_address],
    }

    return filter_params


def get_abi_params() -> list[dict]:
    return [
        {
            "constant": True,
            "inputs": [],
            "name": "symbol",
            "outputs": [{"name": "", "type": "string"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        }
    ]


def get_approval_logs(w3, address: str):
    filter_params = build_get_logs_filter_params(w3, address)
    return w3.eth.get_logs(filter_params)


def extract_symbol(contract):
    token_symbol = None
    try:
        token_symbol = contract.functions.symbol().call()
    except:
        token_symbol = "UnknownERC20"

    return token_symbol


def parse_approved_amount(data):
    return float("inf") if data == BYTES_INFINITE else int.from_bytes(data, "big")


def format_approval_info(log, w3):
    token_contract = w3.eth.contract(address=log["address"], abi=get_abi_params())
    token_symbol = extract_symbol(token_contract)
    approved_amount = parse_approved_amount(log["data"])

    return f"Approval on {token_symbol} on amount of {approved_amount}"


def get_approvals(address: str) -> None:
    w3 = get_w3_instance()
    logs = get_approval_logs(w3, address)

    if not logs:
        print("No ERC20 approvals found.")
        return

    for log in logs:
        print(format_approval_info(log, w3))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get all ERC20 approvals for a given address."
    )
    parser.add_argument(
        "--address",
        type=str,
        required=True,
        help="The public Ethereum address to query.",
    )
    args = parser.parse_args()

    if not environ.get("INFURA_API_KEY"):
        raise ValueError("INFURA_API_KEY environment variable is required.")
    if not Web3.is_address(args.address):
        raise ValueError(f"Invalid address: {args.address}")

    get_approvals(args.address)
