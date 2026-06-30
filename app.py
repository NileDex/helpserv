import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp.classifier import classify
from nlp.entity_extractor import extract_entities
from nlp.response_engine import generate_response

app = Flask(__name__)
CORS(app)

_context = {'last_intent': None, 'unknown_streak': 0}


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'UniHelp API'})


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True)

    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    user_text = data['message'].strip()
    if not user_text:
        return jsonify({'error': 'Empty message'}), 400

    intent, confidence = classify(user_text)
    entities = extract_entities(user_text)

    resolved_intent = intent
    if intent == 'unknown' and _context['last_intent'] and _context['unknown_streak'] < 2:
        resolved_intent = _context['last_intent']

    if resolved_intent != 'unknown':
        _context['last_intent'] = resolved_intent
        _context['unknown_streak'] = 0
    else:
        _context['unknown_streak'] += 1

    entities['_raw'] = user_text
    result = generate_response(resolved_intent, entities)

    return jsonify({
        'intent': resolved_intent,
        'confidence': confidence,
        'entities': entities,
        'response': result['text'],
        'suggestions': result['suggestions'],
    })


if __name__ == '__main__':
    # Railway injects PORT automatically; fallback to 5000 locally
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    print(f'\n UniHelp Flask API running on http://0.0.0.0:{port}\n')
    app.run(host='0.0.0.0', port=port, debug=debug)
