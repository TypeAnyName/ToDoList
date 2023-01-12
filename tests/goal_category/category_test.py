import json
from datetime import datetime

import pytest

from goals.models import GoalCategory
from goals.serializers import GoalCategorySerializer, GoalCategoryCreateSerializer
from tests.factories import GoalCategoryFactory, BoardFactory, BoardParticipantFactory

pytestmark = pytest.mark.django_db


class TestCategory:
    endpoint = '/goals/goal_category/'
    endpoint_list = '/goals/goal_category/list'
    endpoint_create = '/goals/goal_category/create'

    def test_list(self, user_client, user):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        participant = BoardParticipantFactory.create(board=board_, user=user)

        expected_json = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": GoalCategorySerializer((goal_category,), many=True).data
        }

        response = user_client.get(
            self.endpoint_list,
            HTTP_AUTHORIZATION=user_client
        )

        assert response.status_code == 200
        assert response.data == expected_json

    def test_create(self, user_client, user):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        participant = BoardParticipantFactory.create(board=board_, user=user)

        expected_json = {
            "id": goal_category.id + 1,
            "created": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "updated": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "title": goal_category.title,
            "is_deleted": False,
            "board": board_.id
        }

        response = user_client.post(
            self.endpoint_create,
            data=expected_json,
            content_type="application/json",
            HTTP_AUTHORIZATION=user_client
        )

        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_retrieve(self, user, user_client):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        participant = BoardParticipantFactory.create(board=board_, user=user)

        expected_json = {
            "id": goal_category.id,
            "user": {
                "id": goal_category.user.id,
                "username": user.username,
                "first_name": "",
                "last_name": "",
                "email": ""
            },
            "created": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "updated": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "title": goal_category.title,
            "is_deleted": False,
            "board": board_.id
        }

        url = f'{self.endpoint}{goal_category.id}'

        response = user_client.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_delete(self, user, user_client):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        participant = BoardParticipantFactory.create(board=board_, user=user)
        url = f'{self.endpoint}{goal_category.id}'

        response = user_client.delete(url)

        assert response.status_code == 204

