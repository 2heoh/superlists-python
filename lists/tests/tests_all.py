import sys
import time

from django.test import TestCase
from django.urls import resolve

from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_saves_items_only_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class NewListTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        current_list = List.objects.create()

        self.client.post(
            f"/lists/{current_list.id}/add_item",
            data={'item_text': "A new item"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item')
        self.assertEqual(new_item.list, current_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        current_list = List.objects.create()

        response = self.client.post(f"/lists/{current_list.id}/add_item", data={'item_text': "A new item"})

        self.assertRedirects(response, f"/lists/{current_list.id}/")


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        todo_list = List.objects.create()
        response = self.client.get(f'/lists/{todo_list.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_items_in_list(self):
        todo_list = List.objects.create()
        Item.objects.create(text="Item 1", list=todo_list)
        Item.objects.create(text="Item 2", list=todo_list)

        other_list = List.objects.create()
        Item.objects.create(text="Item 3", list=other_list)

        response = self.client.get(f'/lists/{todo_list.id}/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')
        self.assertNotContains(response, 'Item 3')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context['list'], correct_list)


class DBError:
    pass


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items_to_the_database(self):
        todo_list = List()
        todo_list.save()

        first_item = Item()
        first_item.text = "Item the first"
        first_item.list = todo_list
        first_item.save()

        second_item = Item()
        second_item.text = "Second item"
        second_item.list = todo_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, todo_list)

        first_item_from_db = Item.objects.all()[0]
        self.assertEqual(first_item_from_db.text, first_item.text)
        self.assertEqual(first_item_from_db.list, todo_list)

        second_item_from_db = Item.objects.all()[1]
        self.assertEqual(second_item_from_db.text, second_item.text)
        self.assertEqual(second_item_from_db.list, todo_list)
