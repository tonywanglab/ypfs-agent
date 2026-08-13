"""Role split for the chat UI: an anonymous `user` role and a password-gated
`admin` role.

There are no user accounts. Everyone starts as `user`; posting the right
password to /login puts `role=admin` in the Flask session. That is the whole
model — it exists to separate two experiences (plain chat vs. chat that can
rewrite the system prompt and curate golden pairs), not to defend against an
attacker who already has the box.

Two properties worth keeping:

* **Unset HARNESS_ADMIN_PASSWORD disables admin entirely** rather than allowing
  an empty password. current_role() re-reads the env on every call, so clearing
  the variable also revokes sessions that were already admin.
* **The route guard is default-deny.** install_guards() lists the endpoints a
  user may reach and refuses everything else, so a new admin route is protected
  by default instead of by remembering to decorate it.
"""

from __future__ import annotations

import hmac
import os
from functools import wraps

from flask import abort, redirect, request, session, url_for

ROLE_ADMIN = "admin"
ROLE_USER = "user"

SESSION_KEY = "role"

# Endpoints an anonymous `user` may reach. Everything else needs admin.
# Kept here rather than next to the routes so the whole access surface is
# readable in one place.
USER_ENDPOINTS = frozenset({
    "static",
    "chat.login",
    "chat.logout",
    "chat.conversations_list",
    "chat.new_conversation",
    "chat.conversation",
    "chat.post_message",
    "chat.turn_status",
    # A user's own thread is theirs to throw away.
    "chat.delete_conversation",
})


def admin_password() -> str | None:
    """The configured admin password, or None when admin is disabled."""
    return os.environ.get("HARNESS_ADMIN_PASSWORD") or None


def admin_enabled() -> bool:
    return admin_password() is not None


def check_password(candidate: str) -> bool:
    """Constant-time comparison against the configured password.

    Returns False when admin is disabled, so an unset env var can never be
    satisfied by an empty submission.
    """
    expected = admin_password()
    if expected is None:
        return False
    return hmac.compare_digest(candidate or "", expected)


def log_in() -> None:
    session[SESSION_KEY] = ROLE_ADMIN
    session.permanent = False


def log_out() -> None:
    session.pop(SESSION_KEY, None)


def current_role() -> str:
    """`admin` only if the session says so AND admin is still configured."""
    if session.get(SESSION_KEY) == ROLE_ADMIN and admin_enabled():
        return ROLE_ADMIN
    return ROLE_USER


def is_admin() -> bool:
    return current_role() == ROLE_ADMIN


def _deny():
    """Send a navigating browser to the login page; refuse anything else.

    A plain GET is a person who followed a link somewhere they aren't signed in
    for, so redirecting beats a dead end. A POST, an XHR, or a caller that asked
    for JSON is a program, and it gets a flat 403 rather than a 302 to an HTML
    page it can't use.
    """
    is_xhr = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    prefers_json = request.accept_mimetypes.best == "application/json"
    if request.method == "GET" and not is_xhr and not prefers_json:
        return redirect(url_for("chat.login", next=request.full_path))
    abort(403)


def admin_required(view):
    """Guard one view. install_guards() already covers every non-user endpoint;
    this is for readability on the routes where it matters most."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not is_admin():
            return _deny()
        return view(*args, **kwargs)

    return wrapper


def install_guards(app) -> None:
    """Default-deny guard over the whole app.

    Everything outside USER_ENDPOINTS — the eval console, prompt versions, the
    task queue, golden pairs — requires admin.
    """
    @app.before_request
    def _require_admin_outside_user_surface():
        endpoint = request.endpoint
        if endpoint is None:
            return None  # unrouted: let Flask 404 it
        if endpoint in USER_ENDPOINTS:
            return None
        if is_admin():
            return None
        return _deny()
