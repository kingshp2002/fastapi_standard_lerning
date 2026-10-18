from exceptions import EmailAlreadyExistsException, UserNotFoundException
from schemas import UserOutput


def get_user_or_404(users: list[UserOutput], user_id : int):
    existing_user = next((u for u in users if u.id == user_id),None)
    if not existing_user:
        raise UserNotFoundException()
    return existing_user

def email_already_exists(users : list[UserOutput], email : str):
    if any(u.email == email for u in users):
        raise EmailAlreadyExistsException()


def  email_already_exists_update(users : list[UserOutput], email : str, existing_user_id : int):
    if any(u.email == email and u.id != existing_user_id for u in users ):
        raise EmailAlreadyExistsException()