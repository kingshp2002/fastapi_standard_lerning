from exceptions import EmailAlreadyExistsException, UserNotFoundException
from schemas import UserOutput, UserRequest

class UserService:
    def __init__(self, users: list[UserOutput]):
        self.users = users

    def _get_user_or_404(self, user_id: int):
        existing_user = next((user for user in self.users if user.id == user_id), None)
        if not existing_user:
            raise UserNotFoundException()
        return existing_user

    def _email_already_exists(self, email: str):
        if any(user.email == email for user in self.users):
            raise EmailAlreadyExistsException()

    def _email_already_exists_update(self, email: str, user_id: int):
        if any(user.email == email and user.id != user_id for user in self.users):
            raise EmailAlreadyExistsException()

    def get_users(self):
        return self.users

    def create_user(self, user: UserRequest):
        self._email_already_exists(user.email)
        new_user = UserOutput(id=len(self.users) + 1, **user.model_dump())
        self.users.append(new_user)
        return new_user

    def get_user(self, user_id: int):
        return self._get_user_or_404(user_id)

    def update_user(self, user_id: int, user: UserRequest):
        existing_user = self._get_user_or_404(user_id)
        self._email_already_exists_update(user.email, user_id)
        for key, value in user.model_dump().items():
            setattr(existing_user, key, value)
        return existing_user

    def patch_user(self, user_id: int, user: UserRequest):
        existing_user = self._get_user_or_404(user_id)
        self._email_already_exists_update(user.email, user_id)
        for key, value in user.model_dump(exclude_unset=True).items():
        return existing_user

    def delete_user(self, user_id: int):
        existing_user = self._get_user_or_404(user_id)
        self.users.remove(existing_user)
        return existing_user