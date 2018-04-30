from django.test import TestCase
from django.apps import apps
from .apps import TodoConfig

# Create your tests here.
class TestTodoConfig(TestCase):
    def test_app(self):
        self.assertEqual("todo", TodoConfig.name)
        self.assertEqual("todo", apps.get_app_config("todo").name)