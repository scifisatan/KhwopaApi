from fastapi import Request
from schemas import UserLoginSchema
from exceptions import LoginRequiredError

def login_required(request: Request) -> UserLoginSchema:
    """
    Here the validity of the username and password is not checked.
    If the client changes the credentials directly from cookies this will not
    work.
    """
    cookies = request.cookies
    if not cookies:
        raise LoginRequiredError
    
    user_data = UserLoginSchema(**cookies)
    return user_data