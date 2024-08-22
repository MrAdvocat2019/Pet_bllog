from datetime import datetime, timedelta
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from .models import Post

from django.test import Client
client = Client()
class PostModelTest(TestCase):
    def test_get_verbose_month(self):
        x = datetime(year=2020, month=8, day=20, hour=0, minute=0,second=0)
        post = Post(title="Test1", blog_text="Test", pub_date=x)
        c = post.get_verbose_month()
        self.assertEqual(c,'августа')
    def test_get_short_info(self):
        long_text = 'a a a a a a a a a a a a a a a a a a a a a a a a a  a a a a a a a  a a a a a a a a aa a a a a a aa a a a a a a a a aa a a a a aa a a a a a a aa a a a a a a aa a a a a a a a aa a a a a aa a a a a a aa a a a a a aa '
        post = Post(title='test', blog_text=long_text)
        test_case = post.get_short_info()
        self.assertLessEqual(len(test_case.split()), 50)

def create_post(title, days):
    date = timezone.now() + timedelta(days=days)
    return Post.objects.create(title=title, pub_date=date)


class PostListViewTest(TestCase):
    def test_future_post_list(self):
        post = create_post('Future', 2)
        response = self.client.get(reverse('all'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts available")
        self.assertQuerySetEqual(response.context['posts_list'], [])
    def test_pasr_post_list(self):
        post = create_post('Past', -2)
        response = self.client.get(reverse('all'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['posts_list'], [post])
    def test_past_and_future_post_list(self):
        past = create_post('Past', -2)
        future = create_post("Future", 2)
        response = self.client.get(reverse('all'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['posts_list'], [past])

class DetailPostTest(TestCase):
    def test_future_post(self):
        post = create_post('Future', 2)
        url = reverse("detail", args=(post.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
    def test_past_post(self):
        post = create_post('Past', -22)
        url = reverse("detail", args=(post.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.blog_text)
