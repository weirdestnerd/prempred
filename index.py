from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome home @ PremPred!'

# TODO: get current predictions for current gw for user
@app.route('/current-gw')
def current_gw():
    return jsonify({
        'number': 8,
        'games': [{
        'id': 1,
            'started_at': '2024-10-31T15:00:00.000Z',
            'scores': {
                'team1': 3,
                'team2': 2,
            },
            'team1': {
                'full_name': 'arsenal',
                'short_name': 'arsenal',
                'acronym': 'ars',
                'color': 'red',
            },
            'team2': {
                'full_name': 'chelsea',
                'short_name': 'chelsea',
                'acronym': 'che',
                'color': 'blue',
            },
            'user_prediction': 'chelsea',
            'ai_prediction': '',
            'prediction_score': '',
        }],
        'ai_predictions_for_user': [{'a':1}],
    })

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
@app.route('/season')
def season():
    return jsonify([{
        'number': 8,
        'games': [{
        'id': 1,
            'started_at': '2024-10-09T15:00:00.000Z',
            'scores': {
                'team1': 3,
                'team2': 2,
            },
            'team1': {
                'full_name': 'arsenal',
                'short_name': 'arsenal',
                'acronym': 'ars',
                'color': 'red',
            },
            'team2': {
                'full_name': 'chelsea',
                'short_name': 'chelsea',
                'acronym': 'che',
                'color': 'blue',
            },
            'user_prediction': 'chelsea',
            'ai_prediction': '',
            'prediction_score': '',
        }],
        'ai_predictions_for_user': [],
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
