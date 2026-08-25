from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db

industry_bp = Blueprint("industry", __name__)


@industry_bp.route("/industry")
def dashboard():
    session["role"] = "industry"
    challenges = db.get_challenges()
    suggestions = db.get_suggestions()
    by_challenge = {}
    for c in challenges:
        by_challenge[c["id"]] = [s for s in suggestions if s["challenge_id"] == c["id"]]
    return render_template("industry_dash.html", challenges=challenges, by_challenge=by_challenge)


@industry_bp.route("/industry/post", methods=["GET", "POST"])
def post_challenge():
    if request.method == "POST":
        tags = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]
        db.add_challenge(
            company=request.form["company"],
            sector=request.form["sector"],
            workflow=request.form["workflow"],
            challenge=request.form["challenge"],
            tags=tags
        )
        flash("Challenge posted ✓")
        return redirect(url_for("industry.dashboard"))
    return render_template("post_challenge.html")


@industry_bp.route("/industry/mark-interested/<suggestion_id>", methods=["POST"])
def mark_interested(suggestion_id):
    db.mark_interested(suggestion_id)
    flash("Marked as interested — innovator notified")
    return redirect(url_for("industry.dashboard"))
