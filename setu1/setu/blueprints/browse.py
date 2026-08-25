from flask import Blueprint, render_template, session, redirect, url_for
import db

browse_bp = Blueprint("browse", __name__)


@browse_bp.route("/browse")
def browse():
    session["role"] = "innovator"
    challenges = db.get_challenges()
    suggestions = db.get_suggestions()
    counts = {}
    for c in challenges:
        counts[c["id"]] = len([s for s in suggestions if s["challenge_id"] == c["id"]])
    return render_template("browse.html", challenges=challenges, counts=counts)


@browse_bp.route("/challenge/<challenge_id>")
def detail(challenge_id):
    c = db.get_challenge(challenge_id)
    if not c:
        return redirect(url_for("browse.browse"))
    suggestions = db.get_suggestions(challenge_id)
    return render_template("detail.html", c=c, suggestions=suggestions)
