import streamlit as st
import jwt
from jwt import ExpiredSignatureError
from datetime import datetime, timedelta
import extra_streamlit_components as stx

class AuthTokenManager:
    def __init__(
        self,
        cookie_name: str,
        token_key: str,
        token_duration_days: int,
    ):
        self.cookie_manager = stx.CookieManager()
        self.cookie_name = cookie_name
        self.token_key = token_key
        self.token_duration_days = token_duration_days
        self.token = None

    def get_decoded_token(self):
        """Récupère et décode le token d'authentification"""
        self.token = self.cookie_manager.get(self.cookie_name)
        if self.token is None:
            return None
        self.token = self._decode_token()
        return self.token

    def set_token(self, email: str, oauth_id: str):
        """Crée et stocke un token d'authentification"""
        exp_date = (
            datetime.now() + timedelta(days=self.token_duration_days)
        ).timestamp()
        token = self._encode_token(email, oauth_id, exp_date)
        self.cookie_manager.set(
            self.cookie_name,
            token,
            expires_at=datetime.fromtimestamp(exp_date),
        )

    def delete_token(self):
        """Supprime le token d'authentification"""
        try:
            self.cookie_manager.delete(self.cookie_name)
        except KeyError:
            pass

    def _decode_token(self):
        """Décode le token JWT"""
        try:
            decoded = jwt.decode(self.token, self.token_key, algorithms=["HS256"])
            return decoded
        except ExpiredSignatureError:
            st.toast("🔴 Token expiré, veuillez vous reconnecter")
            self.delete_token()
            return None

    def _encode_token(self, email: str, oauth_id: str, exp_date: float) -> str:
        """Encode les informations utilisateur dans un token JWT"""
        encoded = jwt.encode(
            {"email": email, "oauth_id": oauth_id, "exp": exp_date},
            self.token_key,
            algorithm="HS256",
        )
        return encoded
