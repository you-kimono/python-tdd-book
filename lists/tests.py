from django.test import TestCase


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        item_text = 'A new list item'
        response = self.client.post(
            '/',
            data =
                {
                'item_text' : item_text
                }
            )
        self.assertIn(item_text, response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
