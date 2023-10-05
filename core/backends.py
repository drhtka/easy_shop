import logging

from cryptography.hazmat.backends.openssl import backend
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.utils import absolutify
from django.contrib.auth import get_user_model

from accounts.models import Profile

User = get_user_model()

LOGGER = logging.getLogger(__name__)


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """CusRtom OIDC authentication backend."""

    LOGGER.warning("Custom OIDC authentication backend")
    # def filter_users_by_claims(self, claims):
    #     email = claims.get('email')
    #     if not email:
    #         return self.UserModel.objects.none()
    #
    #     try:
    #         profile = Profile.objects.get(email=email)
    #         return [profile.user]
    #
    #     except Profile.DoesNotExist:
    #         return self.UserModel.objects.none()
####

    # def create_user(self, claims, user=None):
    #     """ Overrides Authentication Backend so that Django users are
    #         created with the keycloak preferred_username.
    #         If nothing found matching the email, then try the username.
    #     """
    #     # logger.debug(f"r.url36 :: '{r.url}'")
    #     LOGGER.debug(f"email-39, '{claims.get('email')}'")
    #     check_user = User.objects.filter(email=claims.get('email'))
    #     LOGGER.debug(f"check_user-41, '{check_user}'")
    #     if check_user is None:
    #         LOGGER.debug(f"claims-40, '{check_user}'")
    #         LOGGER.debug(f"claims-41, '{claims}'")
    #         user = super(CustomOIDCAuthenticationBackend, self).create_user(claims)
    #
    #         user.first_name = claims.get('given_name', 'examlp1')
    #         user.last_name = claims.get('family_name', 'examlp2')
    #         user.email = claims.get('email', 'email@email.com')
    #         # user.email = claims.get('email')
    #         user.is_staff = True #Here the fix that error
    #         user.username = claims.get('name', 'examlp')
    #         user.password=backend.generate_random_password()
    #         # user.username = claims.get('preferred_username')
    #         LOGGER.debug(f"user-back-56, '{user.password}'")
    #         user.save()
    #         return user
    #
    #     user = User.objects.filter(email=claims.get('name'))
    #     LOGGER.debug(f"user-back-name-61, '{user}'")
    #     return user
    #
    # def filter_users_by_claims(self, claims):
    #     """ Return all users matching the specified email.
    #         If nothing found matching the email, then try the username
    #     """
    #     LOGGER.debug(f"claims-back-36, '{claims}'")
    #     email = claims.get('email')
    #
    #     if not email:
    #         return self.UserModel.objects.none()
    #     users = self.UserModel.objects.filter(email__iexact=email)
    #     return users
    #
    # def update_user(self, user, claims):
    #     LOGGER.debug(f"claims-45, '{claims}'")
    #     user.first_name = claims.get('given_name', '')
    #     user.last_name = claims.get('family_name', '')
    #     user.email = claims.get('email')
    #     user.save()
    #     return user
    ######https://www.appsloveworld.com/django/100/128/django-oidc-with-keycloak-oidc-callback-state-not-found-in-session-oidc-states

    def authenticate(self, request, **kwargs):
        """Authenticates a user based on the OIDC code flow."""
        self.request = request
        if not self.request:
            return None
        LOGGER.debug(f"request-backends-58, '{request.GET.get}'")

        state = self.request.GET.get("state")
        code = self.request.GET.get("code")
        nonce = kwargs.pop("nonce", None)

        if not code or not state:
            return None

        reverse_url = self.get_settings(
            "OIDC_AUTHENTICATION_CALLBACK_URL", "oidc_authentication_callback"
        )

        token_payload = {
            "client_id": self.OIDC_RP_CLIENT_ID,
            "client_secret": self.OIDC_RP_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": absolutify(self.request, reverse(reverse_url)),
        }
        LOGGER.debug(f"request-backends-79, '{token_payload}'")
        # Get the token
        token_info = self.get_token(token_payload)
        id_token = token_info.get("id_token")
        access_token = token_info.get("access_token")
        refresh_token = token_info.get("refresh_token")
        LOGGER.debug(f"request-backends-116, '{id_token, access_token}'")
        # Validate the token
        payload = self.verify_token(id_token, nonce=nonce)

        if payload:
            self.store_tokens(access_token, id_token, refresh_token) # <--- HERE: store tokens
            try:
                return self.get_or_create_user(access_token, id_token, payload)
            except SuspiciousOperation as exc:
                LOGGER.debug("failed to get or create user: %s", exc)
                return None

        return None

    def store_tokens(self, access_token, id_token, refresh_token): # <--- HERE: store tokens
        """Store OIDC tokens."""
        session = self.request.session
        LOGGER.debug(f"session-backends-133, {session}")

        if self.get_settings("OIDC_STORE_ACCESS_TOKEN", True):
            session["oidc_access_token"] = access_token

        if self.get_settings("OIDC_STORE_ID_TOKEN", False):
            session["oidc_id_token"] = id_token

        if self.get_settings("OIDC_STORE_REFRESH_TOKEN", True): # <--- HERE: Add refresh token option
            session["oidc_refresh_token"] = refresh_token
