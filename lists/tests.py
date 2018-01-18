from django.test import TestCase
from lists.models import Item
from lists.models import List

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        list_ = List.objects.create()
        Item.objects.create(text='item1', list=list_)
        Item.objects.create(text='item2', list=list_)
        other_list_ = List.objects.create()
        Item.objects.create(text='other_item1', list=other_list_)
        Item.objects.create(text='other_item2', list=other_list_)

        response = self.client.get(f'/lists/{list_.id}/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'other_item1')
        self.assertNotContains(response, 'other_item2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item_text = 'Item 1'
        second_item_text = 'Item 2'

        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = first_item_text
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = second_item_text
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, first_item_text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_item_text)
        self.assertEqual(second_saved_item.list, list_)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        item_text = 'A new list item'
        response = self.client.post('/lists/new', data={'item_text' : item_text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirects_after_POST(self):
        item_text = 'A new list item'
        response = self.client.post('/lists/new', data={'item_text' : item_text})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        saved_item = Item.objects.first()
        self.assertEqual(saved_item.text, 'A new item for an existing list')
        self.assertEqual(saved_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
