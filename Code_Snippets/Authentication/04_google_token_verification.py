"""Boxing Canvas — server-side Google ID token verification.

This is a focused excerpt from the FastAPI authentication module. It relies
on application helpers such as _client_id(), _db(), current_user(), and
_public(), which are defined elsewhere in the original module.
"""

from datetime import datetime
from fastapi import HTTPException, Request
from pydantic import BaseModel


class GoogleLogin(BaseModel):
    credential: str


def auth_google(body: GoogleLogin, request: Request):
    """Verify Google's ID token, update the account, and start a session."""
    cid = _client_id()
    if not cid:
        raise HTTPException(
            status_code=503,
            detail="Google login is not configured",
        )

    try:
        from google.auth.transport import requests as google_requests
        from google.oauth2 import id_token
    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="google-auth is not installed",
        )

    try:
        info = id_token.verify_oauth2_token(
            body.credential,
            google_requests.Request(),
            cid,
            clock_skew_in_seconds=10,
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    if not info.get("email_verified", False):
        raise HTTPException(status_code=401, detail="Email not verified")

    now = datetime.now().isoformat(timespec="seconds")
    with _lock, _db() as connection:
        connection.execute(
            """INSERT INTO users(sub,email,name,picture,created_at,last_login)
               VALUES(?,?,?,?,?,?)
               ON CONFLICT(sub) DO UPDATE SET
               email=excluded.email,
               name=excluded.name,
               picture=excluded.picture,
               last_login=excluded.last_login""",
            (
                info["sub"],
                info.get("email", ""),
                info.get("name", ""),
                info.get("picture", ""),
                now,
                now,
            ),
        )

    request.session.clear()
    request.session["sub"] = info["sub"]
    user = current_user(request)
    return {"ok": True, "user": _public(user)}


# The production module also exposes logout and /me endpoints.
