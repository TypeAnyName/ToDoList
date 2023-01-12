import json
from datetime import datetime

import pytest

from goals.models import Board
from goals.serializers import BoardListSerializer, BoardCreateSerializer, BoardSerializer
from tests.factories import BoardFactory, BoardParticipantFactory


# pytestmark = pytest.mark.django_db


class TestBoard:
    endpoint = '/goals/board/'
    endpoint_list = '/goals/board/list'
    endpoint_create = '/goals/board/create'

    @pytest.mark.django_db
    def test_list(self, client, user_client, user):
        board_ = BoardFactory.create(title="test board")
        participant = BoardParticipantFactory.create(board=board_, user=user)

        expected_json = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": BoardListSerializer((board_,), many=True).data
        }

        response = user_client.get(
            self.endpoint_list,
            HTTP_AUTHORIZATION=user_client
        )

        assert response.status_code == 200
        assert response.data == expected_json

    @pytest.mark.django_db
    def test_create(self, client, user_client):
        board = Board.objects.create(
            title="test_board",
        )

        expected_response = {
            "id": board.id + 1,
            "title": board.title,
            "created": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "updated": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "is_deleted": False,
        }

        response = client.post(
            self.endpoint_create,
            data=expected_response,
            format='json',
            HTTP_AUTHORIZATION=user_client
        )

        assert response.status_code == 201
        assert json.loads(response.content) == expected_response

    @pytest.mark.django_db
    def test_retrieve(self, client, user_client, user):
        board_ = BoardFactory.create(title="test board")
        participant = BoardParticipantFactory.create(board=board_, user=user)

        expected_json = {
            "id": board_.id,
            "participants": [
                {
                    "id": participant.id,
                    "role": 1,
                    "user": user.username,
                    "created": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                    "updated": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                    "board": board_.id
                }
            ],
            "created": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "updated": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "title": board_.title,
            "is_deleted": False
        }

        url = f'{self.endpoint}{board_.id}'

        response = user_client.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    @pytest.mark.django_db
    def test_delete(self, client, user_client, user):
        board_ = BoardFactory.create(title="test board")
        participant = BoardParticipantFactory.create(board=board_, user=user)
        url = f'{self.endpoint}{board_.id}'

        response = user_client.delete(url)

        assert response.status_code == 204
