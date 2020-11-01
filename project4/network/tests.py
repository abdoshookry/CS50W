from django.db.models import Max
from django.test import Client, TestCase

from .models import User, posts, follow

# Create your tests here.
class postsTestCase(TestCase):
    def setUp(self):
        f1 = follow(user = User(username = 'abdo'), following = User(username = 'test'))
        f2 = follow(user = User(username = 'test'), following = User(username = 'abdo'))

        p1 = posts(user = User(username = 'abdo'), content="nice")
        p2 = posts(user = User(username = 'test'), content="hello")

    def test_following(self):
        c = Client()
        response = c.get("/following/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["posts"].count(), 2)


