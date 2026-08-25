from flask import Blueprint, render_template, session
import db

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    challenges = db.get_challenges()
    suggestions = db.get_suggestions()
    stats = {
        "industries": len(set(c["company"] for c in challenges)),
        "challenges": len(challenges),
        "suggestions": len(suggestions),
    }
    return render_template("home.html", stats=stats)


@home_bp.route("/switch-role")
def switch_role():
    session.pop("role", None)
    from flask import redirect, url_for
    return redirect(url_for("home.home"))
