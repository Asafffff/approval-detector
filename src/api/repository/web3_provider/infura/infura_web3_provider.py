import logging
from web3 import Web3
from web3.types import LogReceipt, ABI
from src.api.repository.dto.approval_event_response import ApprovalEventResponse
from src.api.repository.web3_provider import web3_provider
from src.api.core.config import settings
from src.constant import BYTES_INFINITE

logger = logging.getLogger(__name__)

# Couldn't understand why they log debug outputs even though my global logging level is set to INFO
# And why they need a special treatment like this. But didn't want to spend too much time on it.
web3_logger = logging.getLogger("web3")
urllib_logger = logging.getLogger("urllib3")
web3_logger.setLevel(logging.INFO)
urllib_logger.setLevel(logging.INFO)


class InfuraWeb3Provider(web3_provider.Web3Provider):
    def __init__(self) -> None:
        super().__init__()
        self.w3 = Web3(
            Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}")
        )

        if not self.w3.is_connected():
            raise ConnectionResetError("Failed to connect to Ethereum network!")

    def list_approvals_by_address(self, address: str) -> list[ApprovalEventResponse]:
        result: list[ApprovalEventResponse] = []
        logs = self._get_approval_logs(self.w3, address)

        if not logs:
            logger.info("No ERC20 approvals found.")
            return

        for eventLog in logs:
            result.append(self.format_approval_info(eventLog))

        return result

    def _build_get_logs_filter_params(self, w3: Web3, address: str) -> dict:
        # Define the ERC-20 token Approval event signature
        approval_signature_hash = w3.keccak(
            text="Approval(address,address,uint256)"
        ).hex()
        padded_address = "0x" + Web3.to_checksum_address(address)[2:].rjust(64, "0")

        filter_params = {
            "fromBlock": "earliest",
            "toBlock": "latest",
            "topics": [approval_signature_hash, padded_address],
        }

        return filter_params

    def _get_abi_params(self) -> list[ABI]:
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

    def _get_approval_logs(self, w3: Web3, address: str):
        filter_params = self._build_get_logs_filter_params(w3, address)

        logger.info(f"Getting ERC20 approval logs for address: {address}")
        logger.debug(f"Filter params: {filter_params}")

        result = w3.eth.get_logs(filter_params)

        logger.info(f"Found {len(result)} ERC20 approval logs for address: {address}")

        return result

    def _extract_symbol(self, contract):
        token_symbol = None

        try:
            token_symbol = contract.functions.symbol().call()
        except:
            token_symbol = "UnknownERC20"

        return token_symbol

    def _parse_approved_amount(self, data: bytes):
        return float("inf") if data == BYTES_INFINITE else int.from_bytes(data, "big")

    def format_approval_info(self, eventLog: LogReceipt) -> ApprovalEventResponse:
        token_contract = self.w3.eth.contract(
            address=eventLog["address"], abi=self._get_abi_params()
        )
        token_symbol = self._extract_symbol(token_contract)
        approved_amount = self._parse_approved_amount(eventLog["data"])

        return ApprovalEventResponse(
            token_symbol=token_symbol,
            amount=-1 if approved_amount == float("inf") else approved_amount,
            is_infinite=approved_amount == float("inf"),
        )
