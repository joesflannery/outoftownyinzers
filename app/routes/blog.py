from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from ..auth import require_admin
from ..db import get_db

bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route("/")
def index():
    db = get_db()
    all_posts = db.execute(
        "SELECT * FROM posts WHERE published = 1 ORDER BY created_at DESC"
    ).fetchall()
    return render_template("blog_reader.html", post=all_posts[0] if all_posts else None, all_posts=all_posts)


@bp.route("/<int:post_id>")
def post(post_id):
    db = get_db()
    row = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if row is None:
        abort(404)
    all_posts = db.execute(
        "SELECT * FROM posts WHERE published = 1 ORDER BY created_at DESC"
    ).fetchall()
    return render_template("blog_reader.html", post=row, all_posts=all_posts)


@bp.route("/new", methods=["GET", "POST"])
@require_admin
def new():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        body = request.form.get("body", "").strip()
        if not title or not author or not body:
            flash("Title, author, and body are all required.", "error")
            return render_template("blog_form.html", post=request.form, form_title="New Post")
        db = get_db()
        cur = db.execute(
            "INSERT INTO posts (title, body, author) VALUES (?, ?, ?)",
            (title, body, author),
        )
        db.commit()
        flash("Post published.", "info")
        return redirect(url_for("blog.post", post_id=cur.lastrowid))
    return render_template("blog_form.html", post=None, form_title="New Post")


@bp.route("/<int:post_id>/edit", methods=["GET", "POST"])
@require_admin
def edit(post_id):
    db = get_db()
    row = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if row is None:
        abort(404)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        body = request.form.get("body", "").strip()
        if not title or not author or not body:
            flash("Title, author, and body are all required.", "error")
            return render_template("blog_form.html", post=request.form, form_title="Edit Post", post_id=post_id)
        db.execute(
            "UPDATE posts SET title = ?, author = ?, body = ? WHERE id = ?",
            (title, author, body, post_id),
        )
        db.commit()
        flash("Post updated.", "info")
        return redirect(url_for("blog.post", post_id=post_id))
    return render_template("blog_form.html", post=row, form_title="Edit Post", post_id=post_id)


@bp.route("/<int:post_id>/delete", methods=["POST"])
@require_admin
def delete(post_id):
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    flash("Post deleted.", "info")
    return redirect(url_for("blog.index"))
