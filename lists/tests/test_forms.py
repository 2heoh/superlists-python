from unittest import TestCase

from lists.forms import ItemForm
from lists.models import List, Item


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ["You can't have an empty list item"])

    def test_form_validation_for_non_empty_items(self):
        form = ItemForm(data={'text': 'text'})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_form_save_handles_saving_to_a_list(self):
        todo_list = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=todo_list)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, todo_list)
