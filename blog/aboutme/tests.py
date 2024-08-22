from django.test import Client, TestCase
from django.urls import reverse
client = Client()
class AboutMeTest(TestCase):
    def test_about_me_view(self):
        response = client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MyPhoto.jpeg')