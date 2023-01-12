import json
from datetime import datetime
import factory
from django.utils.timezone import now

import pytest

from goals.models import Goal, GoalCategory, Board
from goals.serializers import GoalSerializer, GoalCreateSerializer

from tests.factories import GoalFactory, BoardFactory, BoardParticipantFactory, GoalCategoryFactory

pytestmark = pytest.mark.django_db


class TestGoal:
    endpoint = '/goals/goal/'
    endpoint_list = '/goals/goal/list'
    endpoint_create = '/goals/goal/create'

    @pytest.mark.django_db
    def test_list(self, user_client, user):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        goal_ = GoalFactory.create(title="test", user=user, category=goal_category)
        participant = BoardParticipantFactory.create(board=board_, user=user)

        expected_json = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": GoalSerializer((goal_,), many=True).data
        }

        response = user_client.get(
            self.endpoint_list,
            HTTP_AUTHORIZATION=user_client
        )

        assert response.status_code == 200
        assert response.data == expected_json

    @pytest.mark.django_db
    def test_create(self, client, user_client, user, goal):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        goal_ = GoalFactory.create(title="test", user=user, category=goal_category)
        participant = BoardParticipantFactory.create(board=board_, user=user)

        expected_json = {
            "id": goal_.id + 1,
            "category": goal_category.id,
            "created": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "updated": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "title": goal_.title,
            "description": "",
            "status": 1,
            "priority": 2,
            "due_date": None
        }

        response = user_client.post(
            self.endpoint_create,
            data=expected_json,
            content_type="application/json",
            HTTP_AUTHORIZATION=user_client
        )

        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    @pytest.mark.django_db
    def test_retrieve(self, user_client, user):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        goal_ = Goal.objects.create(title="test", user=user, category=goal_category)
        participant = BoardParticipantFactory.create(board=board_, user=user)

        expected_json = {
            "id": goal_.id,
            "category": goal_category.id,
            "created": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "updated": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "title": goal_.title,
            "description": goal_.description,
            "status": 1,
            "priority": 2,
            "due_date": goal_.due_date,
            "user": goal_.user.id
        }

        url = f'{self.endpoint}{goal_.id}'

        response = user_client.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    @pytest.mark.django_db
    def test_delete(self, user_client, user):
        board_ = BoardFactory.create(title="test board")
        goal_category = GoalCategoryFactory.create(title="test_category", user=user, board=board_)
        goal_ = Goal.objects.create(title="test", user=user, category=goal_category)
        participant = BoardParticipantFactory.create(board=board_, user=user)
        url = f'{self.endpoint}{goal_.id}'

        response = user_client.delete(url)

        assert response.status_code == 204
