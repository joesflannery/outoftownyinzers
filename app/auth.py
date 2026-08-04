"""
Session-based auth for the small admin-only corner of the site (posting to
the blog). Active only when ADMIN_PASSWORD is set in the environment --
locally that isn't set, so posting is wide open for development. On
PythonAnywhere you set it as a WSGI env var and the new/edit/delete blog
routes redirect to a login page instead.

One shared password, not a username/password pair -- this gates a single
"can post to the blog" capability shared by Joe and Justin, not individual
accounts.

Session-based (a normal login page + cookie) rather than HTTP Basic Auth
(the browser's native popup) -- the fantasy football app's /live page hit
real problems with Basic Auth being flaky against background polling, so
this avoids that class of bug here too.

Unlike the rest of the site (Home/News/Blog reading/Shop), which is public
with no login at all, this only wraps the specific write routes via the
@require_admin decorator -- see app/routes/blog.py and the /admin/login,
/admin/logout routes in app/routes/main.py.
"""

import os
from functools import wraps

from flask import request, session, redirect, url_for


def admin_password_configured():
    return bool(os.environ.get("ADMIN_PASSWORD"))


def check_password(password):
    expected = os.environ.get("ADMIN_PASSWORD")
    return expected is not None and password == expected


def require_admin(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not admin_password_configured():
            return view(*args, **kwargs)  # not configured -- no auth (local dev)
        if not session.get("is_admin"):
            return redirect(url_for("main.admin_login", next=request.path))
        return view(*args, **kwargs)

    return wrapped
