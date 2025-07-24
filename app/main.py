from flask import Flask, request, jsonify, redirect
from app.models import URLStore
from app.utils import is_valid_url

app = Flask(__name__)
store = URLStore()

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url or not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400

    short_code = store.create_short_url(original_url)
    return jsonify({
        'short_code': short_code,
        'short_url': f'http://localhost:5000/{short_code}'
    })

@app.route('/<short_code>')
def redirect_url(short_code):
    url = store.get_original_url(short_code)
    if url:
        store.increment_clicks(short_code)
        return redirect(url)
    return jsonify({'error': 'Short code not found'}), 404

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    stats = store.get_stats(short_code)
    if not stats:
        return jsonify({'error': 'Short code not found'}), 404
    return jsonify(stats)

@app.route('/health')
def health():
    return jsonify({'status': 'OK'})
