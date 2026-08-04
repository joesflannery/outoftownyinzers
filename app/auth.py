"""
HTTP Basic Auth for the small admin-only corner of the site (posting to the
blog). Active only when ADMIN_USERNAME/ADMIN_PASSWORD are set in the
environment -- locally those aren't set, so posting is wide open for
development. On PythonAnywhere you set them as WSGI env vars and the
new/edit/delete blog routes get gated behind a browser login prompt.

Unlike the rest of the site (Home/News/Blog reading/Shop), which is public
with no login at all, this only wraps the specific write routes via the
@require_admin decorator -- see app/routes/blog.py.
"""

import os
from functools import wraps

from flask import request, Response


def _check_auth(username, password):
    expected_user = os.environ.get("ADMIN_USERNAME")
    expected_pass = os.environ.get("ADMIN_PASSWORD")
    return username == expected_user and password == expected_pass


def _unauthorized():
    return Response(
        "Login required.", 401, {"WWW-Authenticate": 'Basic realm="Yinzers Admin"'}
    )


def require_admin(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not os.environ.get("ADMIN_USERNAME") or not os.environ.get("ADMIN_PASSWORD"):
            return view(*args, **kwargs)  # not configured -- no auth (local dev)
        auth = request.authorization
        if not auth or not _check_auth(auth.username, auth.password):
            return _unauthorized()
        return view(*args, **kwargs)

    return wrapped
