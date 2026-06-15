import pytest
from app import app, distances


@pytest.fixture(autouse=True)
def clear_distances():
    distances.clear()
    yield
    distances.clear()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_html_get(client):
    response = client.get('/')
    assert response.status_code == 200


def test_html_post(client):
    response = client.post('/', data={'apoint': '4,0', 'bpoint': '0,0'})
    assert response.status_code == 200
    assert len(distances) == 1
    assert distances[0]['result_distance'] == 4.0


def test_api_index(client):
    response = client.get('/api')
    assert response.status_code == 200
    assert response.get_json() == {}


def test_api_distances_empty(client):
    response = client.get('/api/distances')
    assert response.status_code == 200
    assert response.get_json() == []


def test_api_distances_with_data(client):
    client.post('/', data={'apoint': '3,4', 'bpoint': '0,0'})
    response = client.get('/api/distances')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['result_distance'] == 5.0


def test_calculate(client):
    response = client.post(
        '/api/distance',
        json={'start_point': '0,0', 'end_point': '3,4'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['result_distance'] == 5.0
    assert data['start_point'] == [0, 0]
    assert data['end_point'] == [3, 4]
