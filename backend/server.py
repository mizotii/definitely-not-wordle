import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

load_dotenv()
frontend_host = os.environ.get('FRONTEND_HOST', 'http://localhost:5173')

app = Flask(__name__)
CORS(
    app,
    resources = {
        r'/api/*': {'origins': frontend_host}
    }
)

@app.route('/api/hello')
def hello():
    return jsonify({ 'message': 'hello world' }), 200

if __name__ == '__main__':
    app.run()