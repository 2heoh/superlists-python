from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    todo_list = List.objects.get(id=list_id)
    items = Item.objects.filter(list=todo_list)
    return render(request, 'list.html', {'items': items, 'list': todo_list})


def new_list(request):
    todo_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=todo_list)
    return redirect(f"/lists/{todo_list.id}/")


def add_item(request, list_id):
    todo_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=todo_list)
    return redirect(f"/lists/{todo_list.id}/")
