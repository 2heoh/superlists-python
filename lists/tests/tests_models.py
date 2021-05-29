from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


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

    def test_cannot_save_emtpy_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
