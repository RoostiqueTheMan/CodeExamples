"""Module with authentication operations."""

import os
from datetime import datetime, timedelta
from typing import Dict, Optional

import jwt
from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext

from authorization_app import models

__all__ = [
    'JWTToken',
    'Password',
]


EXPIRATION_TIME_DAYS = 30
COOKIE_KEY = os.getenv('COOKIE_KEY')


class JWTToken:
    """Class with methods for working with JWT token."""

    def __init__(
        self,
        cypher_algorithm: str = 'HS256',
        secret_key: str = 'salt'
    ):
        """Initialize class method.

        :param cypher_algorithm: Cyther algorythm type
        :param secret_key: salt key
        """
        self.__secret_key = secret_key
        self.__cypher_algorithm = cypher_algorithm

    def create(self, user: models.User) -> str:
        """Create JWT token from name and password hash.

        Args:
            user: User

        Returns: JWT token
        """
        payload = {
            'sub': 'auth',
            'exp': datetime.now() + timedelta(days=EXPIRATION_TIME_DAYS),
            'name': user.name,
            'password_hash': user.password
        }
        return jwt.encode(
            payload=payload,
            key=self.__secret_key,
            algorithm=self.__cypher_algorithm
        )

    def verify(self, token: str) -> Dict[str, str]:
        """Verify JWT token.

        Args:
            token: str

        Returns: dict
        """
        try:
            return jwt.decode(
                jwt=token,
                key=self.__secret_key,
                algorithms=[self.__cypher_algorithm]
            )
        except jwt.PyJWTError:
            return {}


class Password:
    """Class with password operations."""

    def __init__(self, password: str, cypher_schema: str = 'sha256_crypt'):
        """Initializing method.

        Args:
            password: password
            cypher_schema: cypher schema
        """
        self.__pwd_context = CryptContext(schemes=[cypher_schema])
        self.__password = password

    @property
    def hashed_password(self) -> str:
        """Create hashed password.

        Returns: hashed password
        """
        return self.__pwd_context.hash(secret=self.__password)

    def verify(self, password_hash: str) -> bool:
        """Verify password.

        Args:
            password_hash: password hash

        Returns: True if verified, otherwise False
        """
        return self.__pwd_context.verify(
            secret=self.__password, hash=password_hash
        )


class OAuth2PasswordBearerWithCookie(OAuth2):
    """Changed basic FastAPI class, which check auth by cookie."""
    def __init__(self, tokenUrl: str,
                 scheme_name: Optional[str] = None,
                 scopes: Optional[Dict[str, str]] = None,
                 description: Optional[str] = None,
                 auto_error: bool = True,):
        """Initializing method.

        Args:
            tokenUrl: get token endpoint
            scheme_name: scheme name
            scopes: scopes
            description: description
            auto_error: bool
        """
        if not scopes:
            scopes = {}
        flows = OAuthFlows(
            password={'tokenUrl': tokenUrl, 'scopes': scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        """Method check token existing in cookie.

        Args:
            request: Request

        Returns: param
        """
        authorization: str = request.cookies.get(COOKIE_KEY)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != 'bearer':
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Not authenticated',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            else:
                return None

        return param