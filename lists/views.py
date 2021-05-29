from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    todo_list = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=todo_list)
            item.full_clean()
            item.save()
            return redirect(todo_list)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, 'list.html', {'list': todo_list, 'error': error})


def new_list(request):
    todo_list = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=todo_list)
    try:
        item.full_clean()
    except ValidationError:
        todo_list.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})

    return redirect(todo_list)
