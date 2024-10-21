from audioop import error

from flask import Flask, jsonify, request, abort
from marshmallow import ValidationError

from model.user import UserSchema, UserDB
from service.gameweek import GameweekService

app = Flask(__name__)

@app.errorhandler(422)
def unprocessable_entity(e):
    return jsonify(error=str(e)), 422

# E.g. 'GET /user?username=abc'
@app.route('/user')
def get_user():
    user_params = request.args

    if 'username' not in user_params.keys():
        abort(422, description="Missing required param: username")

    try:
        user = UserDB.find({ 'username': user_params['username'] } )
    except error:
        abort(422, description="Something went wrong finding this user!")

    return jsonify(user), 200

@app.route('/user', methods=['POST'])
def create_user():
    # TODO: only admin users can create users
    user_params = request.args
    schema = UserSchema()

    try:
        user = schema.load(user_params)
        user = UserDB.create(user)
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
