import os
import secrets
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from helpers import guess_word, is_correct, sanitize_guess
from typing import Dict, List
from wordle import WordList

MAX_TURNS = 6

load_dotenv()
frontend_host = os.environ.get('FRONTEND_HOST', 'http://localhost:5173')

app = Flask(__name__)
CORS(
    app,
    resources={r'/api/.*': {'origins': frontend_host}},
    allow_headers=['Content-Type', 'X-Session-Token'],
)

word_list = WordList()
game_sessions: Dict[str, dict] = {}

@app.route('/api/game/start', methods=['POST'])
def start():
    token = secrets.token_urlsafe(32)
    game_sessions[token] = {
        'current_answer': word_list.replace_current_answer(),
        'current_turn_number': 0,
        'game_status': 'in_progress',
        'guess_history': [{'': []} for _ in range(MAX_TURNS)],
    }
    gs = game_sessions[token]
    return jsonify({
        'token': token,
        'current_turn_number': gs['current_turn_number'],
        'game_status': gs['game_status'],
        'guess_history': gs['guess_history'],
    }), 200

@app.route('/api/game', methods=['GET'])
def status():
    token = request.headers.get('X-Session-Token')
    gs = game_sessions.get(token)
    if not gs:
        return jsonify({'message': 'No session found. Try pressing reset'}), 404
    return jsonify({
        'current_turn_number': gs['current_turn_number'],
        'game_status': gs['game_status'],
        'guess_history': gs['guess_history'],
    }), 200

@app.route('/api/guess', methods=['POST'])
def guess():
    token = request.headers.get('X-Session-Token')
    gs = game_sessions.get(token)
    if not gs:
        return jsonify({'message': 'No session found. Try pressing reset'}), 404

    guess = sanitize_guess(request.get_json()['guess'])
    if not guess:
        return jsonify({'is_valid_guess': False, 'message': 'Invalid input'}), 400

    if not word_list.is_valid_guess(guess):
        return jsonify({
            'is_valid_guess': False,
            'message': 'Not in word list!',
            'current_turn_number': gs['current_turn_number'],
            'game_status': gs['game_status'],
            'guess_history': gs['guess_history'],
        }), 200

    result = guess_word(guess, gs['current_answer'])
    gs['guess_history'][gs['current_turn_number']] = {guess: result}
    gs['current_turn_number'] += 1

    if is_correct(result):
        gs['game_status'] = 'won'
    elif gs['current_turn_number'] >= MAX_TURNS:
        gs['game_status'] = 'lost'

    response = {
        'is_valid': True,
        'current_turn_number': gs['current_turn_number'],
        'game_status': gs['game_status'],
        'guess_history': gs['guess_history'],
        'message': ' ',
    }
    if gs['game_status'] != 'in_progress':
        response['current_answer'] = gs['current_answer']
        response['message'] = f"You {gs['game_status']}. The word was: {gs['current_answer']}"

    return jsonify(response), 200

if __name__ == '__main__':
    app.run()
