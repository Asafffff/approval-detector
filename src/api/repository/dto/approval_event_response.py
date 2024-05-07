from pydantic import BaseModel


class ApprovalEventResponse(BaseModel):
    token_symbol: str
    amount: int
    is_infinite: bool
