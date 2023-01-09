import factory

from core.models import User
from goals.models import Board, GoalCategory, Goal, GoalComment

from django.utils.timezone import now


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    password = "abcabc123123"


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = "test"


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = "test"
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = "test"
    description = "test description"
    due_date = factory.LazyAttribute(lambda x: now())
    status = 2
    priority = 2
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)


class GoalCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)
    text = 'test comment text'