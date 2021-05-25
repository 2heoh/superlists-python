from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    todo_list = List.objects.get(id=list_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=todo_list)
        return redirect(f'/lists/{todo_list.id}/')
    return render(request, 'list.html', {'list': todo_list})
    # items = Item.objects.filter(list=todo_list)
    # return render(request, 'list.html', {'items': items, 'list': todo_list})


def new_list(request):
    todo_list = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=todo_list)
    try:
        item.full_clean()
    except ValidationError:
        todo_list.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(f"/lists/{todo_list.id}/")
