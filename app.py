import logging
import traceback
import yaml
import os

from flask import Flask, request, jsonify
from typing import Dict, List, Union, Optional
import json
import datetime
from flask_cors import CORS

from api_boardgame_gpt import init_boardgame, follow_up, start_game, game_round

# Load configuration from YAML file
def load_config(config_file='config.yaml'):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Initialize application with configuration
config = load_config()
app = Flask(__name__)

# Configure CORS from config
CORS(app,
     resources=config['cors']['resources'],
     methods=config['cors']['methods'])

# Configure logging from config
logging.basicConfig(level=getattr(logging, config['logging']['level']))
logger = logging.getLogger(__name__)

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
@app.route('/api/v1/rules/generate', methods=['POST', 'OPTIONS'])
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
    if request.method == 'OPTIONS':
        return '', 204  # Respond to the OPTIONS request
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
        description_of_background = data['description_of_background']
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
        logger.error(f"Error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


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
        logger.error(f"Error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/v1/gameplay/start', methods=['POST'])
def start_gameplay():
    """
    Start a new gameplay session.
    Required fields:
    - rule_id (int)
    - player_role (str)
    """
    try:
        data = request.get_json()
        # Validate required fields
        if 'rule_id' not in data or 'player_role' not in data:
            return jsonify({'error': 'Missing required fields: rule_id and player_role'}), 400

        # Type validation
        if not isinstance(data['rule_id'], int):
            return jsonify({'error': 'rule_id must be an integer'}), 400

        # Implementation
        rule_id = data['rule_id']
        player_role = data['player_role']
        file_path_rule = "return/board_game_id_" + str(rule_id) + "_follow.json"
        start_game_content = start_game(rule_id, file_path_rule, player_role)

        return jsonify({
            "rule_id": rule_id,
            "name": start_game_content['name'],
            "player_role": start_game_content['player_role'],
            "history": start_game_content['history'],
            "next_action": start_game_content['next_action']
        })

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/v1/gameplay/round', methods=['POST'])
def simulate_round():
    try:
        logger.debug("Received request data")
        data = request.get_json()
        logger.debug(f"Request data: {data}")

        # Validate required fields
        required_fields = ['rule_id', 'action', 'round_id']
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400

        logger.debug("Passed field validation")

        # Type validation
        if not isinstance(data['rule_id'], int):
            logger.error("Invalid rule_id type")
            return jsonify({'error': 'rule_id must be an integer'}), 400
        if not isinstance(data['round_id'], int):
            logger.error("Invalid round_id type")
            return jsonify({'error': 'round_id must be an integer'}), 400

        logger.debug("Passed type validation")

        # Implementation
        rule_id = data['rule_id']
        round_id = data['round_id']
        action = data['action']

        file_path_rule = "return/board_game_id_" + str(rule_id) + "_follow.json"
        file_path_history = "return/board_game_id_" + str(rule_id) + "_history.json"

        logger.debug(f"Attempting to read files: {file_path_rule}, {file_path_history}")

        round_content = game_round(rule_id, file_path_rule, file_path_history, round_id, action)
        logger.debug(f"game_round returned: {round_content}")

        return jsonify({
            "rule_id": rule_id,
            "name": round_content['name'],
            "player_role": round_content['player_role'],
            "history": round_content['history'],
            "next_action": round_content['next_action']
        })

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


if __name__ == '__main__':
    server_config = config['server']
    app.run(
        debug=server_config['debug'],
        host=server_config['host'],
        port=server_config['port']
    )