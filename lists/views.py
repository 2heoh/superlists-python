from django.shortcuts import render, redirect

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)

    if form.is_valid():
        todo_list = List.objects.create()
        form.save(for_list=todo_list)
        return redirect(todo_list)
    else:
        return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    todo_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=todo_list)
    if request.method == 'POST':
        form = ExistingListItemForm(
            for_list=todo_list,
            data=request.POST
        )
        if form.is_valid():
            form.save()
            return redirect(todo_list)

    return render(request, 'list.html', {'list': todo_list, 'form': form})
