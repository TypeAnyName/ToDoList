def test_root_not_found(client):
    response = client.get("/")

    assert response.status_code == 404


def test_board_list(client, test_token):
    response = client.get(
        '/board/board/list',
        HTTP_AUTHORIZATION=test_token
    )

    assert response.status_code == 200


def test_goal_category_list(client, test_token):
    response = client.get(
        '/board/goal_category/list',
        HTTP_AUTHORIZATION=test_token
    )

    assert response.status_code == 200


def test_goal_list(client, test_token):
    response = client.get(
        '/board/goal/list',
        HTTP_AUTHORIZATION=test_token
    )

    assert response.status_code == 200



