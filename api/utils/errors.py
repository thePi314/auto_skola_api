from typing import TypedDict, Dict

from rest_framework import status


class Error:
    code: str
    message: str
    http_status_code: int

    def __init__(self, code: str, message: str, http_status_code: int = None):
        self.code = code
        self.message = message
        self.http_status_code = http_status_code


EMAIL_NOT_VERIFIED = "emailNotVerified"
VERIFICATION_TOKEN_INVALID = "verificationTokenInvalid"
USER_BY_TOKEN_MISSING = 'userNOtFoundByToken'
USER_PASS_INVALID = "userPasswordInvalid"
STRIPE_SIGNATURE_FAILED = "stripeSignatureFailed"
LOGIN_IS_BLOCKED = "loginIsBlocked"
ACCOUNT_DISABLED = "accountDisabled"
INVALID_CREDENTIALS = "invalidCredentials"
TOKEN_EXPIRED = "tokenExpired"
USER_IS_ALREADY_ADMIN = "userAlreadyAnAdmin"
USER_IS_NOT_ADMIN = "userIsNotAnAdmin"


ERRORS: Dict[str, Error] = {
    VERIFICATION_TOKEN_INVALID: Error(VERIFICATION_TOKEN_INVALID, "Verification token does not exists", status.HTTP_400_BAD_REQUEST),
    USER_BY_TOKEN_MISSING: Error(USER_BY_TOKEN_MISSING, "User with provided token does not exist", status.HTTP_400_BAD_REQUEST),
    EMAIL_NOT_VERIFIED: Error(EMAIL_NOT_VERIFIED, "Email address not verified", status.HTTP_403_FORBIDDEN),
    USER_PASS_INVALID: Error(USER_PASS_INVALID, "User password is not valid.", status.HTTP_400_BAD_REQUEST),
    STRIPE_SIGNATURE_FAILED: Error(STRIPE_SIGNATURE_FAILED, "Stripe webhook signature failed!", status.HTTP_400_BAD_REQUEST),
    LOGIN_IS_BLOCKED: Error(LOGIN_IS_BLOCKED, "Login is blocked.", status.HTTP_400_BAD_REQUEST),
    INVALID_CREDENTIALS: Error(INVALID_CREDENTIALS, "Invalid credentials.", status.HTTP_400_BAD_REQUEST),
    TOKEN_EXPIRED: Error(TOKEN_EXPIRED, "This token is expired.", status.HTTP_400_BAD_REQUEST),
    USER_IS_ALREADY_ADMIN: Error(USER_IS_ALREADY_ADMIN, "User is already an admin", status.HTTP_400_BAD_REQUEST),
    USER_IS_NOT_ADMIN: Error(USER_IS_NOT_ADMIN, "User is not an admin", status.HTTP_400_BAD_REQUEST),
}
