from fastapi import APIRouter


router = APIRouter()


@router.get("")
def health():
    return {"message": "Server is up and running"}
