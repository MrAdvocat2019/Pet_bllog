from datetime import datetime, timedelta
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from .models import Post
from categories.models import Category
from django.test import Client
client = Client()


class PostModelTest(TestCase):
    def test_get_verbose_month(self):
        x = datetime(year=2020, month=8, day=20, hour=0, minute=0, second=0)
        post = Post(title="Test1", blog_text="Test", pub_date=x)
        c = post.get_verbose_month()
        self.assertEqual(c, 'августа')

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

    def test_question_with_wrongcategory_notappears_when_filtered(self):
        cat1 = Category.objects.create(name="Testcat1")
        cat2 = Category.objects.create(name="Testcat2")
        # This post should only be associated with cat1
        post = create_post("TestPost1", -1)
        post.categories.add(cat1)

        # Request with a category that the post does not belong to
        response = self.client.get(
            reverse('all'), {'categories': [str(cat2.pk)]})

        # Assert that no posts are returned
        self.assertQuerySetEqual(response.context['posts_list'], [])

    def test_question_with_wrongcategory_appears_when_filtered(self):
        cat1 = Category.objects.create(name="Testcat1")
        # This post should only be associated with cat1
        post = create_post("TestPost1", -1)
        post.categories.add(cat1)

        # Request with a category that the post does not belong to
        response = self.client.get(
            reverse('all'), {'categories': [str(cat1.pk)]})

        # Assert that no posts are returned
        self.assertQuerySetEqual(response.context['posts_list'], [post])

    def test_question_with_wrongcategory_appears_when_filtered_twice(self):
        cat1 = Category.objects.create(name="Testcat1")
        cat2 = Category.objects.create(name="TestCat2")
        # This post should only be associated with cat1
        post = create_post("TestPost1", -1)
        post.categories.add(cat1)
        post.categories.add(cat2)

        # Request with a category that the post does not belong to
        response = self.client.get(
            reverse('all'), {'categories': [str(cat1.pk), str(cat2.pk)]})

        # Assert that no posts are returned
        self.assertQuerySetEqual(response.context['posts_list'], [post])

    def test_question_with_wrongcategory_notappears_when_filtered_twice(self):
        cat1 = Category.objects.create(name="Testcat1")
        cat2 = Category.objects.create(name="TestCat2")
        # This post should only be associated with cat1
        post = create_post("TestPost1", -1)
        post.categories.add(cat1)

        # Request with a category that the post does not belong to
        response = self.client.get(
            reverse('all'), {'categories': [str(cat1.pk), str(cat2.pk)]})

        # Assert that no posts are returned
        self.assertQuerySetEqual(response.context['posts_list'], [])

    def test_too_early_post(self):
        post = Post.objects.create(
            title='Tst', blog_text="123", pub_date='2024-8-2')
        date_start = '2024-08-03'
        response = self.client.get(reverse('all'), {'date_start': date_start})
        self.assertQuerySetEqual(response.context['posts_list'], [])

    def test_too_late_post(self):
        post = Post.objects.create(
            title='Tst', blog_text="123", pub_date='2024-8-4')
        date_finish = '2024-08-03'
        response = self.client.get(
            reverse('all'), {'date_finish': date_finish})
        self.assertQuerySetEqual(response.context['posts_list'], [])

    def test_just_right_post(self):
        post = Post.objects.create(
            title='Tst', blog_text="123", pub_date='2024-8-2')
        date_start = '2024-08-01'
        date_finish = '2024-08-03'
        response = self.client.get(
            reverse('all'), {'date_finish': date_finish, 'date_start': date_start})
        self.assertQuerySetEqual(response.context['posts_list'], [post])

    def test_right_cat_right_date(self):
        cat1 = Category.objects.create(name="Testcat1")
        post = Post.objects.create(
            title='Tst', blog_text="123", pub_date='2024-8-2')
        post2 = Post.objects.create(
            title='2', blog_text="23", pub_date='2024-07-01')
        post.categories.add(cat1)
        date_start = '2024-08-01'
        date_finish = '2024-08-03'
        response = self.client.get(reverse('all'), {
                                   'date_finish': date_finish, 'date_start': date_start, 'categories': [str(cat1.pk),]})
        self.assertQuerySetEqual(response.context['posts_list'], [post])

    def test_right_cat_wrong_date(self):
        cat1 = Category.objects.create(name="Testcat1")
        post = Post.objects.create(
            title='Tst', blog_text="123", pub_date='2024-7-01')
        post2 = Post.objects.create(
            title='2', blog_text="23", pub_date='2024-07-01')
        post.categories.add(cat1)
        date_start = '2024-08-01'
        date_finish = '2024-08-03'
        response = self.client.get(reverse('all'), {
                                   'date_finish': date_finish, 'date_start': date_start, 'categories': [str(cat1.pk),]})
        self.assertQuerySetEqual(response.context['posts_list'], [])

    def test_wrong_cat_right_date(self):
        cat1 = Category.objects.create(name="Testcat1")
        cat2 = Category.objects.create(name="Testcat2")
        post = Post.objects.create(
            title='Tst', blog_text="123", pub_date='2024-7-01')
        post2 = Post.objects.create(
            title='2', blog_text="23", pub_date='2024-07-01')
        post.categories.add(cat1)
        date_start = '2024-08-01'
        date_finish = '2024-08-03'
        response = self.client.get(reverse('all'), {
                                   'date_finish': date_finish, 'date_start': date_start, 'categories': [str(cat2.pk),]})
        self.assertQuerySetEqual(response.context['posts_list'], [])


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

    def test_category(self):
        cat1 = Category.objects.create(name="Testcat1")
        # This post should only be associated with cat1
        post = create_post("TestPost1", -1)
        post.categories.add(cat1)
        response = self.client.get(reverse('detail', args=(post.id,)))
        self.assertContains(response, cat1.name)
