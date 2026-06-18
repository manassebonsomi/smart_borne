from flask import Flask
from flask_cors import CORS
from models import *
from config.database import db

from routes.auth_routes import auth_routes
from routes.command_routes import command_bp
from routes.profile_routes import profile_bp
from routes.recommendation_routes import recommandation_bp
from routes.dashboard_routes import dashboard_routes
from routes.survey_routes import survey_routes
from routes.question_routes import question_bp
from routes.utilisateur_routes import utilisateur_bp
from routes.campagne_routes import campagne_bp
from routes.erreur_routes import erreur_bp
from routes.report_routes import report_bp

app = Flask(__name__)

app.register_blueprint(auth_routes, url_prefix="/api")
app.register_blueprint(command_bp, url_prefix="/api")
app.register_blueprint(profile_bp, url_prefix="/api")
app.register_blueprint(question_bp, url_prefix="/api")
app.register_blueprint(utilisateur_bp, url_prefix="/api")
app.register_blueprint(campagne_bp, url_prefix="/api")
app.register_blueprint(erreur_bp, url_prefix="/api")
app.register_blueprint(report_bp, url_prefix="/api")
app.register_blueprint(recommandation_bp, url_prefix="/api")
app.register_blueprint(dashboard_routes, url_prefix="/api")
app.register_blueprint(survey_routes, url_prefix="/api")

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = \
'mysql+pymysql://root:343877@localhost/db_ccc_orientation_system'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Création automatique des tables
# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True)