from django.test import TestCase

from lists.models import Item, List


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



