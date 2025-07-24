import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'OK'

def test_shorten_and_redirect(client):
    res = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert res.status_code == 200
    data = res.get_json()
    short_code = data['short_code']

    redirect_res = client.get(f'/{short_code}', follow_redirects=False)
    assert redirect_res.status_code == 302

def test_invalid_url(client):
    res = client.post('/api/shorten', json={'url': 'not-a-url'})
    assert res.status_code == 400

def test_stats(client):
    res = client.post('/api/shorten', json={'url': 'https://example.com'})
    short_code = res.get_json()['short_code']

    for _ in range(3):
        client.get(f'/{short_code}')

    stats_res = client.get(f'/api/stats/{short_code}')
    stats = stats_res.get_json()
    assert stats['clicks'] == 3
    assert stats['url'] == 'https://example.com'
    assert 'created_at' in stats

def test_404_on_unknown_code(client):
    res = client.get('/api/stats/unknown123')
    assert res.status_code == 404
