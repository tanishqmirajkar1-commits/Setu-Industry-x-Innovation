from flask import Flask

from blueprints.home import home_bp
from blueprints.browse import browse_bp
from blueprints.suggestions import suggestions_bp
from blueprints.industry import industry_bp
import db
from seed_data import SEED_CHALLENGES

app = Flask(__name__)
app.secret_key = "hackathon-demo-secret-change-me"

app.register_blueprint(home_bp)
app.register_blueprint(browse_bp)
app.register_blueprint(suggestions_bp)
app.register_blueprint(industry_bp)

with app.app_context():
    db.init_db(SEED_CHALLENGES)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
