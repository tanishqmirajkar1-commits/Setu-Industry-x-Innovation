from flask import Blueprint, request, redirect, url_for, flash
import db

suggestions_bp = Blueprint("suggestions", __name__)


@suggestions_bp.route("/suggestions/submit", methods=["POST"])
def submit():
    challenge_id = request.form["challenge_id"]
    name = request.form["name"]
    title = request.form["title"]
    desc = request.form["desc"]
    db.add_suggestion(challenge_id, name, title, desc)
    flash("Suggestion submitted ✓")
    return redirect(url_for("browse.detail", challenge_id=challenge_id))
