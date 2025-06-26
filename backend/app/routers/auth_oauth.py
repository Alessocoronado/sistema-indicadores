from fastapi import APIRouter, Request, Header, HTTPException
from fastapi.responses import RedirectResponse
import os
import msal
import requests
from jose import jwt

router = APIRouter(tags=["auth"])

CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
TENANT_ID = os.getenv("AZURE_TENANT_ID", "common")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = os.getenv("AZURE_REDIRECT_URI", "http://localhost:8000/auth/callback")
SCOPE = ["User.Read"]

msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)

@router.get("/login")
def login():
    auth_url = msal_app.get_authorization_request_url(
        SCOPE, redirect_uri=REDIRECT_URI
    )
    return RedirectResponse(auth_url)

@router.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")
    result = msal_app.acquire_token_by_authorization_code(
        code, scopes=SCOPE, redirect_uri=REDIRECT_URI
    )
    if "access_token" in result:
        return {
            "access_token": result["access_token"],
            "id_token": result.get("id_token"),
        }
    raise HTTPException(status_code=400, detail=result.get("error_description"))

JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"

def _get_signing_key(kid: str):
    jwks = requests.get(JWKS_URL).json()
    for key in jwks["keys"]:
        if key.get("kid") == kid:
            return key
    return None

@router.post("/verify-token")
def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization header")
    token = authorization.split(" ", 1)[1]
    try:
        headers = jwt.get_unverified_header(token)
        key = _get_signing_key(headers["kid"])
        if not key:
            raise Exception("Signing key not found")
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
        )
        return {"valid": True, "payload": payload}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
