from abc import ABC, abstractmethod

from src.api.repository.dto.approval_event_response import ApprovalEventResponse


class Web3Provider(ABC):
    @abstractmethod
    def list_approvals_by_address(self, address: str) -> list[ApprovalEventResponse]:
        pass
