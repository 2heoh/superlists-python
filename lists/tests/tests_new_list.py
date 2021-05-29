from django.test import TestCase

from lists.models import Item, List


class NewListTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        current_list = List.objects.create()

        self.client.post(
            f"/lists/{current_list.id}/",
            data={'text': "A new item"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item')
        self.assertEqual(new_item.list, current_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        current_list = List.objects.create()

        response = self.client.post(
            f"/lists/{current_list.id}/",
            data={'text': "A new item"}
        )

        self.assertRedirects(response, f"/lists/{current_list.id}/")
