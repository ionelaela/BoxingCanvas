"""Boxing Canvas — per-user canvas ownership and access control.

These excerpts show how a canvas is associated with a signed-in account
and how the application distinguishes account-owned canvases from guest
canvases. Database and authentication helpers belong to the main app module.
"""

import os
from datetime import datetime
from fastapi import HTTPException, Request
from pydantic import BaseModel


def allowed(owner, user):
    """Allow users to see their own canvases and guests to see unowned ones."""
    if user:
        return owner == user["sub"]
    return owner is None


class Claim(BaseModel):
    id: str


def claim_canvas(body: Claim, request: Request):
    """Associate an existing local canvas with the current user's account."""
    user = current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Sign in required")

    # Reduce the supplied identifier to a folder name before using it in a path.
    session_id = os.path.basename(body.id)
    if not _has_artwork(session_id):
        raise HTTPException(status_code=404, detail="Canvas not found")

    with _lock, _db() as connection:
        connection.execute(
            """INSERT OR IGNORE INTO canvases(session_id,user_sub,claimed_at)
               VALUES(?,?,?)""",
            (
                session_id,
                user["sub"],
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        row = connection.execute(
            "SELECT user_sub FROM canvases WHERE session_id=?",
            (session_id,),
        ).fetchone()

    if row["user_sub"] != user["sub"]:
        raise HTTPException(
            status_code=403,
            detail="Canvas belongs to another account",
        )

    return {"ok": True}


# Gallery endpoints call allowed(owner_of(session_id), current_user(request))
# before returning canvas metadata or permitting deletion.
