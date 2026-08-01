"""Authentication service implementing the multi-step login flow.

Flow per PDF specification:
1. User enters username → system verifies
2. If valid, user enters password → system verifies
3. If valid, system generates and displays a random verification code
4. User inputs the verification code → system checks match
5. If correct, access is granted with a "Welcome" message
"""

from electronics_store.models.user import User
from electronics_store.data.store_data import get_users
from electronics_store.utils.helpers import generate_verification_code


class AuthService:
    def __init__(self) -> None:
        self._users: dict[str, User] = {u.username: u for u in get_users()}
        self._current_user: User | None = None
        self._verification_code: str = ""

    def verify_username(self, username: str) -> tuple[bool, str]:
        username = username.strip()
        if username in self._users:
            return True, "Username verified. Please enter your password."
        return False, "Username not found. Please try again."

    def verify_password(self, username: str, password: str) -> tuple[bool, str]:
        user = self._users.get(username.strip())
        if user is None:
            return False, "Username not found."
        if user.password == password:
            self._verification_code = generate_verification_code()
            return True, self._verification_code
        return False, "Incorrect password. Please try again."

    def verify_code(self, username: str, code: str) -> tuple[bool, str]:
        if code.strip() == self._verification_code:
            self._current_user = self._users.get(username.strip())
            display = self._current_user.display_name if self._current_user else username
            return True, f"Welcome, {display}!"
        return False, "Verification code does not match. Please try again."

    @property
    def current_user(self) -> User | None:
        return self._current_user

    @property
    def verification_code(self) -> str:
        return self._verification_code

    def logout(self) -> None:
        self._current_user = None
        self._verification_code = ""
