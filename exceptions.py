from fastapi import status, HTTPException


class LoginRequiredError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login required to view this page."
        )