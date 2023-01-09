import json
import pytest

from goals.models import GoalComment
from goals.serializers import GoalCommentSerializer, GoalCommentCreateSerializer
from tests.factories import GoalCommentFactory

pytestmark = pytest.mark.django_db


class TestComment:
    endpoint = '/goals/goal_comment/'
    endpoint_list = '/goals/goal_comment/list'
    endpoint_create = '/goals/goal_comment/create'

    def test_list(self, api_client, user_client):
        comments = GoalCommentFactory.create_batch(10)

        expected_json = {
            "count": 10,
            "next": None,
            "previous": None,
            "results": GoalCommentSerializer(comments, many=True).data
        }

        response = api_client().get(
            self.endpoint_list,
            HTTP_AUTHORIZATION=user_client
        )

        assert response.status_code == 200
        assert response.data == expected_json

    def test_create(self, api_client, user_client):
        comments = GoalCommentFactory.create_batch(10)

        expected_json = {
            "count": 10,
            "next": None,
            "previous": None,
            "results": GoalCommentCreateSerializer(comments, many=True).data
        }

        response = api_client().post(
            self.endpoint_create,
            data=expected_json,
            format='json',
            HTTP_AUTHORIZATION=user_client
        )

        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_retrieve(self, api_client, user_client, comment):
        comments = GoalCommentFactory.create_batch(1)

        expected_json = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": GoalCommentSerializer(comments, many=True).data
        }

        url = f'{self.endpoint}{comment.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_delete(self, api_client, user_client, comment):
        url = f'{self.endpoint}{comment.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert GoalComment.objects.all().count() == 0