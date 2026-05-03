import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from helpers import guess_word, is_correct, sanitize_guess
from typing import Dict, List
from wordle import WordList

MAX_TURNS = 6

load_dotenv()
frontend_host = os.environ.get('FRONTEND_HOST', 'http://localhost:5173')
is_production = os.environ.get('FLASK_ENV') == 'production'
secret_key = os.environ.get('SECRET_KEY', None)

if not secret_key:
    raise RuntimeError('SECRET_KEY environment variable not set')

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = is_production
CORS(
    app,
    resources = {
        r'/api/.*': {'origins': frontend_host}
    }
)

word_list = WordList()

@app.route('/api/game/start', methods=['POST'])
def start():
    guess_history: List[Dict[str, List[str]]] = []

    session['current_answer'] = word_list.replace_current_answer()
    session['current_turn_number'] = 0
    session['game_status'] = 'in_progress'
    session['guess_history'] = guess_history

    session.modified = True

    return jsonify({
        'current_turn_number': session['current_turn_number'],
        'game_status': session['game_status'],
        'guess_history': session['guess_history']
    }), 200

@app.route('/api/game', methods=['GET'])
def status():
    if session:
        return jsonify({
            'current_turn_number': session['current_turn_number'],
            'game_status': session['game_status'],
            'guess_history': session['guess_history']
        }), 200
    
    else:
        return jsonify({ 'message': 'No session -- call /api/game/start' }), 404
    
@app.route('/api/guess', methods=['POST'])
def guess():
    if session:
        guess = sanitize_guess(request.get_json()['guess'])
        if not guess:
            return jsonify({
                'is_valid_guess': False,
                'message': 'Invalid input',
            }), 400

        session.modified = True

        if not word_list.is_valid_guess(guess):
            return jsonify({
                'is_valid_guess': False,
                'message': 'Invalid guess!',
            }), 200

        result = guess_word(guess, session['current_answer'])
        session['guess_history'].append({guess: result})
        session['current_turn_number'] += 1

        if is_correct(result):
            session['game_status'] = 'won'

        elif session['current_turn_number'] >= MAX_TURNS:
            session['game_status'] = 'lost'

        session.modified = True

        return jsonify({
            'is_valid': True,
            'current_turn_number': session['current_turn_number'],
            'game_status': session['game_status'],
            'guess_history': session['guess_history'],
        }), 200
    
    else:
        return jsonify({ 'message': 'No session -- call /api/game/start' }), 404

@app.route('/api/hello')
def hello():
    return jsonify({ 'message': 'hello world' }), 200

if __name__ == '__main__':
    app.run()

    