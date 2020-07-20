from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Todo
from api.serializers import TodoSerializer

TODO_URL = reverse('api:todo-list')


def detail_url(todo_id):
    '''Return todo task detail URL'''
    return reverse('api:todo-detail', args=[todo_id])


def sample_todo(user, **params):
    '''Create and return a sample todo task'''
    defaults = {
        'title': 'Sample todo task',
        'text': 'Check all codebase',
        'due_date': datetime(2020, 7, 15, tzinfo=timezone.utc)
    }
    defaults.update(params)

    return Todo.objects.create(user=user, **defaults)


class PublicTodoApiTests(TestCase):
    '''Test unauthenticated todo API access'''

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        '''Test that authentication is required'''
        res = self.client.get(TODO_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoApiTests(TestCase):
    '''Test unauthenticated todo API access'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'a.collins@todo.net',
            '@TEi2^9OuvS'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_todo_tasks(self):
        '''Test retrieving a list of todo tasks'''
        sample_todo(user=self.user)
        sample_todo(user=self.user)

        res = self.client.get(TODO_URL)

        todo = Todo.objects.all()
        serializer = TodoSerializer(todo, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_todo_task_detail(self):
        '''Test viewing a todo task detail'''
        todo = sample_todo(user=self.user)

        url = detail_url(todo.id)
        res = self.client.get(url)

        serializer = TodoSerializer(todo)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_todo_task(self):
        '''Test creating todo task'''
        payload = {
            'title': 'Sample todo task',
            'text': 'Check all codebase',
            'due_date': datetime(2020, 7, 15, tzinfo=timezone.utc)
        }
        res = self.client.post(TODO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        todo = Todo.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(todo, key))

    def test_partial_update_todo_task(self):
        '''Test updating a todo task with patch'''
        todo = sample_todo(user=self.user)

        payload = {'title': 'Next todo task'}
        url = detail_url(todo.id)
        self.client.patch(url, payload)

        todo.refresh_from_db()
        self.assertEqual(todo.title, payload['title'])

    def test_full_update_todo_task(self):
        '''Test updating a todo task with put'''
        todo = sample_todo(user=self.user)
        payload = {
            'title': 'Next todo task',
            'text': 'Create new program',
            'due_date': datetime(2020, 10, 1, tzinfo=timezone.utc)
        }
        url = detail_url(todo.id)
        self.client.put(url, payload)

        todo.refresh_from_db()
        self.assertEqual(todo.title, payload['title'])
        self.assertEqual(todo.text, payload['text'])
        self.assertEqual(todo.due_date, payload['due_date'])
