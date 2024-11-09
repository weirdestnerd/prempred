import os
from audioop import error

from flask import Flask, jsonify, request, abort
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from marshmallow import ValidationError
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

from db.util import get_db_engine
from model import initialize_sql
from model_marshmallow.user import UserSchema
from service.gameweek import GameweekService
from service.user import UserService

login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
bcrypt = Bcrypt(app)
engine = get_db_engine()
initialize_sql(engine)


# Configure application to store JWTs in cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

# Only allow JWT cookies to be sent over https. In production, this
# should likely be True
app.config['JWT_COOKIE_SECURE'] = False # NOTE

# Set the cookie paths, so that you are only sending your access token
# cookie to the access endpoints, and only sending your refresh token
# to the refresh endpoint. Technically this is optional, but it is in
# your best interest to not send additional cookies in the request if
# they aren't needed.
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

# Enable csrf double submit protection. See this for a thorough
# explanation: http://www.redotheweb.com/2015/11/09/api-security.html
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = os.getenv('AUTH_TOKEN_GEN_KEY'),

jwt = JWTManager(app)

@app.errorhandler(422)
def unprocessable_entity(e):
    return jsonify(error=str(e)), 422

# With JWT_COOKIE_CSRF_PROTECT set to True, set_access_cookies() and
# set_refresh_cookies() will now also set the non-httponly CSRF cookies
# as well
@app.route('/token/auth')
def login():
    user_params = request.args

    if 'username' not in user_params.keys():
        abort(422, description="Missing required param: username")

    try:
        user = UserService.get_user(('username', user_params['username']))

        if user and bcrypt.check_password_hash(user.password, user_params['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            responseObject = jsonify({
                'status': 'success',
                'message': 'Successfully logged in.',
            })

            set_access_cookies(responseObject, access_token)
            set_refresh_cookies(responseObject, refresh_token)

            # url_has_allowed_host_and_scheme should check if the url is safe
            # for redirects, meaning it matches the request host.
            # See Django's url_has_allowed_host_and_scheme for an example.
            if request.args.get('next') or not url_has_allowed_host_and_scheme(request.args.get('next'), request.host):
                return abort(422, description="Redirect not allowed")

            return responseObject, 200
        else:
            abort(422, description="User not found")
    except error:
        abort(422, description="Something went wrong logging in this user!")


@app.route('/user', methods=['POST'])
def create_user():
    # TODO: only admin users can create users
    user_params = request.args
    schema = UserSchema()

    try:
        user = schema.load(user_params)
        UserService.create_user(user)
    except ValidationError as error:
        abort(422, description=error.messages)

    return jsonify({"message": "user created", 'user': user}), 200

@app.route('/')
def home():
    return 'Welcome home @ PremPred!'

@app.route('/current-gw')
def current_gw():
    return jsonify(GameweekService().current_gw())

# TODO: get entire leaderboard
@app.route('/leaderboard')
def leaderboard():
    return jsonify([
        {
            'user_name': 'olu',
            'current_game_week_points': 40,
            'total_points': 140,
        },
        {
            'user_name': 'gift',
            'current_game_week_points': 10,
            'total_points': 140,
        },
        {
            'user_name': 'max',
            'current_game_week_points': 50,
            'total_points': 140,
        }
    ])

# TODO: get predictions so far this season for user
#   - paginate by gameweek
@app.route('/season')
def season():
    return jsonify([{
        'number': 8,
        'games': [{
        'id': 1,
            'started_at': '2024-10-09T15:00:00.000Z',
            'scores': {
                'home_team': 3,
                'away_team': 2,
            },
            'home_team': {
                'full_name': 'arsenal',
                'short_name': 'arsenal',
                'acronym': 'ars',
                'color': 'red',
            },
            'away_team': {
                'full_name': 'chelsea',
                'short_name': 'chelsea',
                'acronym': 'che',
                'color': 'blue',
            },
            'user_prediction': 'chelsea',
            'ai_prediction': '',
        }],
    }])


@app.route('/predict-game', methods=['POST'])
def predict_game():
    # TODO: create/update prediction for game for user
    print("PREDICTED!!!")
    return {}, 200

@app.route('/predict-gameweek', methods=['POST'])
def predict_gameweek():
    # TODO: go thru each game in provided gw & create/update prediction for game for user
    return {}, 200

@app.route('/acknowledge-ai', methods=['POST'])
def acknowledge_ai():
    # TODO: save per user 'do not show' ai banner
    return {}, 200
