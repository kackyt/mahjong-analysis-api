import os
from typing import Any, Dict

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
AUTH0_SCOPE = os.environ.get("AUTH0_SCOPE")

ALGORITHMS = ["RS256"]
CACHE_JWK_KEY = None

token_auth_scheme = HTTPBearer()
jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
jwks_client = jwt.PyJWKClient(jwks_url)


async def verify_token(
    token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
) -> Dict[str, Any]:
    if AUTH0_DOMAIN is None:
        return {}

    try:
        rsa_key = jwks_client.get_signing_key_from_jwt(token.credentials).key
    except jwt.exceptions.PyJWKClientError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except jwt.exceptions.DecodeError as e:
        raise HTTPException(status_code=400, detail=e.__str__())

    try:
        payload = jwt.decode(
            token.credentials,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )

        if "scope" in payload:
            token_scopes = payload["scope"].split()

            if AUTH0_SCOPE not in token_scopes:
                raise Exception("permission denied")
        else:
            raise Exception("permission denied")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return payload
