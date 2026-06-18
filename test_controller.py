from app import app

from controllers.profile_controller \
    import ProfileController

with app.app_context():
    utilisateurs = \
        ProfileController.get_all()

    print(utilisateurs)