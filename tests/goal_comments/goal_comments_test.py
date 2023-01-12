import json
from datetime import datetime

import pytest

from goals.models import GoalComment
from goals.serializers import GoalCommentSerializer, GoalCommentCreateSerializer
from tests.factories import GoalCommentFactory, BoardFactory, GoalCategoryFactory, GoalFactory, BoardParticipantFactory

pytestmark = pytest.mark.django_db


class TestComment:
    endpoint = '/goals/goal_comment/'
    endpoint_list = '/goals/goal_comment/list'
    endpoint_create = '/goals/goal_comment/create'

    def test_list(self, user_client, user):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        goal_ = GoalFactory.create(title="test", user=user, category=goal_category)
        participant = BoardParticipantFactory.create(board=board_, user=user)
        comment = GoalCommentFactory.create(text="test text", user=user, goal=goal_)

        expected_json = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": GoalCommentSerializer((comment,), many=True).data
        }

        response = user_client.get(
            self.endpoint_list,
            HTTP_AUTHORIZATION=user_client
        )

        assert response.status_code == 200
        assert response.data == expected_json

    def test_create(self, user, user_client):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        goal_ = GoalFactory.create(title="test", user=user, category=goal_category)
        participant = BoardParticipantFactory.create(board=board_, user=user)
        comment = GoalCommentFactory.create(text="test text", user=user, goal=goal_)

        expected_json = {
            "id": comment.id + 1,
            "created": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "updated": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "text": comment.text,
            "goal": goal_.id
        }
        response = user_client.post(
            self.endpoint_create,
            data=expected_json,
            format='json',
            HTTP_AUTHORIZATION=user_client
        )

        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_retrieve(self, user, user_client):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        goal_ = GoalFactory.create(title="test", user=user, category=goal_category)
        participant = BoardParticipantFactory.create(board=board_, user=user)
        comment = GoalCommentFactory.create(text="test text", user=user, goal=goal_)

        expected_json = {
            "id": comment.id,
            "user": {
                "id": comment.user.id,
                "username": user.username,
                "first_name": "",
                "last_name": "",
                "email": ""
            },
            "created": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "updated": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "text": comment.text,
            "goal": goal_.id
        }
        url = f'{self.endpoint}{comment.id}'

        response = user_client.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_delete(self, user, user_client):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        goal_ = GoalFactory.create(title="test", user=user, category=goal_category)
        participant = BoardParticipantFactory.create(board=board_, user=user)
        comment = GoalCommentFactory.create(text="test text", user=user, goal=goal_)
        url = f'{self.endpoint}{comment.id}'

        response = user_client.delete(url)

        assert response.status_code == 204
