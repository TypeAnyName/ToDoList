import pytest

pytestmark = pytest.mark.django_db

def test_root_not_found(client):
    response = client.get("/")

    assert response.status_code == 404


def test_board_list(user_client):
    response = user_client.get(
        '/goals/board/list',
        HTTP_AUTHORIZATION=user_client
    )

    assert response.status_code == 200


def test_goal_category_list(user_client):
    response = user_client.get(
        '/goals/goal_category/list',
        HTTP_AUTHORIZATION=user_client
    )

    assert response.status_code == 200


def test_goal_list(user_client):
    response = user_client.get(
        '/goals/goal/list',
        HTTP_AUTHORIZATION=user_client
    )

    assert response.status_code == 200



