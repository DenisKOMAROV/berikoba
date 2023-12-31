import pytest
import requests


BASE_URL = "http://127.0.0.1:8000"

def test_root():
    api_url = f"{BASE_URL}"

    response = requests.get(api_url)
    data = response.json()

    assert response.status_code == 200

    assert data["message"] == "I am Berikoba. Welcome!"

def test_get_all_movies():
    api_url = f"{BASE_URL}/movies"

    response = requests.get(api_url)
    data = response.json()

    assert response.status_code == 200

    assert data == [
        "Lord of the Rings",
        "Hobbit",
    ]

get_movie_test_data = [
    (0, "Lord of the Rings"),
    (1, "Hobbit"),
]

@pytest.mark.parametrize("movie_id, movie_name", get_movie_test_data)
def test_get_movie(movie_id, movie_name):
    api_url = f"{BASE_URL}/movies/{movie_id}"

    response = requests.get(api_url)
    data = response.json()

    assert response.status_code == 200

    assert data == {
                    "name": movie_name,
                    "likes": 0,
                    "dislikes": 0,
                    }

def test_add_movie():
    api_url = f"{BASE_URL}/movies/2"
    
    assert get_number_of_movies() == 2

    response = requests.post(api_url, json={"name": "Lore of the Things"})
    assert response.status_code == 200

    assert get_number_of_movies() == 3

def get_number_of_movies():
    api_url = f"{BASE_URL}/movies"

    response = requests.get(api_url)
    data = response.json()

    assert response.status_code == 200

    return len(data)


@pytest.mark.parametrize("movie_id, movie_name", get_movie_test_data)
def test_likes(movie_id, movie_name):
    api_url = f"{BASE_URL}/movies/{movie_id}/score"
    params = {
            "movie_id": movie_id,
            "user_score": "like",
            }

    response = requests.post(api_url, params=params)
    assert response.status_code == 200

    data = response.json()
    
    assert data["movie_id"] == movie_id
    assert data["score"] == "like"
    assert data["likes"] == 1


@pytest.mark.parametrize("movie_id, movie_name", get_movie_test_data)
def test_dislikes(movie_id, movie_name):
    api_url = f"{BASE_URL}/movies/{movie_id}/score"
    params = {
            "movie_id": movie_id,
            "user_score": "dislike",
            }

    response = requests.post(api_url, params=params)
    assert response.status_code == 200

    data = response.json()
    
    assert data["movie_id"] == movie_id
    assert data["score"] == "dislike"
    assert data["dislikes"] == 1
