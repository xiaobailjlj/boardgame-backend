from flask import Flask, request, jsonify
from typing import Dict, List, Union, Optional
import json
import datetime

from api_boardgame_gpt import init_boardgame, follow_up, start_game, game_round

app = Flask(__name__)


# Error handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad Request',
        'message': str(error)
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': str(error)
    }), 404


# API endpoints
@app.route('/api/v1/rules/generate', methods=['POST'])
def generate_rules():
    """
    Generate game rules based on input parameters.
    Required fields:
    - number_of_players (int)
    - game_duration (str)
    - description_of_background (str)
    - game_category (str)
    - game_mechanics (list)
    """
    try:
        data = request.get_json()
        # Validate required fields
        required_fields = ['number_of_players', 'game_duration',
                           'description_of_background', 'game_category',
                           'game_mechanics']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Type validation
        if not isinstance(data['number_of_players'], int):
            return jsonify({'error': 'number_of_players must be an integer'}), 400
        if not isinstance(data['game_mechanics'], list):
            return jsonify({'error': 'game_mechanics must be a list'}), 400

        # Implementation
        number_of_players = data['number_of_players']
        game_duration = data['game_duration']
        description_of_background = "Fight for medical resources in plague cities"
        game_category = data['game_category']
        game_mechanics = data['game_mechanics']
        rule_id = int(datetime.datetime.now().timestamp())

        init_content = init_boardgame(rule_id, number_of_players, game_duration, description_of_background, game_category, game_mechanics)

        return jsonify({
            "rule_id": rule_id,
            "name": init_content['name'],
            "background": init_content['background'],
            "rules": init_content['rules'],
            "players": init_content['players'],
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/rules/optimize', methods=['POST'])
def optimize_rules():
    """
    Optimize existing game rules based on feedback.
    Required fields:
    - rule_id (int)
    - feedback (str)
    """
    try:
        data = request.get_json()
        # Validate required fields
        if 'rule_id' not in data or 'feedback' not in data:
            return jsonify({'error': 'Missing required fields: rule_id and feedback'}), 400

        # Type validation
        if not isinstance(data['rule_id'], int):
            return jsonify({'error': 'rule_id must be an integer'}), 400

        # Implementation
        rule_id = data['rule_id']
        feedback = data['feedback']

        file_path_follow = "return/board_game_id_" + str(rule_id) + "_follow.json"

        updated_content = follow_up(rule_id, file_path_follow, feedback)

        return jsonify({
            "rule_id": rule_id,
            "name": updated_content['name'],
            "background": updated_content['background'],
            "rules": updated_content['rules'],
            "players": updated_content['players']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/api/v1/gameplay/start', methods=['POST'])
# def start_gameplay():
#     """
#     Start a new gameplay session.
#     Required fields:
#     - rule_id (int)
#     - player_role (str)
#     """
#     try:
#         data = request.get_json()
#         # Validate required fields
#         if 'rule_id' not in data or 'player_role' not in data:
#             return jsonify({'error': 'Missing required fields: rule_id and player_role'}), 400
#
#         # Type validation
#         if not isinstance(data['rule_id'], int):
#             return jsonify({'error': 'rule_id must be an integer'}), 400
#
#         # Implementation goes here
#
#         return jsonify({
#             "rule_id": data['rule_id'],
#             "name": "",
#             "player_role": data['player_role'],
#             "history": [],
#             "next_action": {
#                 "choice 1": "",
#                 "choice 2": "",
#                 "choose": ""
#             }
#         })
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#
# @app.route('/api/v1/gameplay/round', methods=['POST'])
# def simulate_round():
#     """
#     Simulate a gameplay round.
#     Required fields:
#     - rule_id (int)
#     - player_role (str)
#     - round_id (int)
#     """
#     try:
#         data = request.get_json()
#         # Validate required fields
#         required_fields = ['rule_id', 'player_role', 'round_id']
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({'error': f'Missing required field: {field}'}), 400
#
#         # Type validation
#         if not isinstance(data['rule_id'], int):
#             return jsonify({'error': 'rule_id must be an integer'}), 400
#         if not isinstance(data['round_id'], int):
#             return jsonify({'error': 'round_id must be an integer'}), 400
#
#         # Implementation goes here
#
#         return jsonify({
#             "rule_id": data['rule_id'],
#             "name": "",
#             "player_role": data['player_role'],
#             "history": [],
#             "next_action": {
#                 "choice 1": "",
#                 "choice 2": "",
#                 "choose": ""
#             }
#         })
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)