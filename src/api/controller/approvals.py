from web3 import Web3
from fastapi import APIRouter, Depends, HTTPException

from src.api.model.response import APIResponse
from src.api.service.approvals_detector import ApprovalDetectionService

router = APIRouter()


@router.get("", response_model=APIResponse)
def list_approvals_by_address(
    address: str,
    service: ApprovalDetectionService = Depends(ApprovalDetectionService),
) -> APIResponse:
    if not Web3.is_address(address):
        raise HTTPException(400, detail=f"Invalid address: {address}")

    result = service.list_approvals_by_address(address)

    return APIResponse(data=result)
