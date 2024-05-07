import logging

from src.api.repository.dto.approval_event_response import ApprovalEventResponse
from src.api.repository.web3_provider.web3_provider import Web3Provider
from src.api.repository.web3_provider.web3_provider_factory import Web3ProviderFactory

logger = logging.getLogger(__name__)


class ApprovalDetectionService:
    def __init__(self):
        self.web3_provider: Web3Provider = Web3ProviderFactory().create()

    def list_approvals_by_address(self, address: str) -> list[ApprovalEventResponse]:
        logger.info(f"Service: Listing approvals for address: {address}")
        result = self.web3_provider.list_approvals_by_address(address)
        logger.info(f"Service: Found {len(result)} approvals for address: {address}")

        return result
