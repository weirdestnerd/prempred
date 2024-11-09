from flask_login import login_manager
from service.user import UserService


class FlaskLoginUtil:

    @login_manager.user_loader
    def load_user(user_id):
        return UserService.get_user(('id', user_id))