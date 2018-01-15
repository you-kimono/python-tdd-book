from django.test import TestCase
from lists.models import Item

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        item_text = 'A new list item'
        response = self.client.post('/', data={'item_text' : item_text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirects_after_POST(self):
        item_text = 'A new list item'
        response = self.client.post('/', data={'item_text' : item_text})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        item_text = 'A new list item'
        response = self.client.get(
            '/',
            data =
                {
                'item_text' : item_text
                }
            )
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_lists_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/')

        self.assertIn('item1', response.content.decode())
        self.assertIn('item2', response.content.decode())


    def test_saving_and_retrieving_items(self):
        first_item_text = 'Item 1'
        second_item_text = 'Item 2'

        first_item = Item()
        first_item.text = first_item_text
        first_item.save()

        second_item = Item()
        second_item.text = second_item_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, first_item_text)
        self.assertEqual(second_saved_item.text, second_item_text)
