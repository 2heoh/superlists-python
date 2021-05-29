from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')


class ListModelTest(TestCase):
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    # def test_saving_and_retrieving_items_to_the_database(self):
    #     todo_list = List()
    #     todo_list.save()
    #
    #     first_item = Item()
    #     first_item.text = "Item the first"
    #     first_item.list = todo_list
    #     first_item.save()
    #
    #     second_item = Item()
    #     second_item.text = "Second item"
    #     second_item.list = todo_list
    #     second_item.save()
    #
    #     saved_list = List.objects.first()
    #     self.assertEqual(saved_list, todo_list)
    #
    #     first_item_from_db = Item.objects.all()[0]
    #     self.assertEqual(first_item_from_db.text, first_item.text)
    #     self.assertEqual(first_item_from_db.list, todo_list)
    #
    #     second_item_from_db = Item.objects.all()[1]
    #     self.assertEqual(second_item_from_db.text, second_item.text)
    #     self.assertEqual(second_item_from_db.list, todo_list)

    def test_cannot_save_emtpy_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()
            # item.save()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')

        item.full_clean()
        item.save()

        expected = Item.objects.all()
        self.assertEqual(expected[0].text, 'bla')
        self.assertEqual(expected[1].text, 'bla')

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
