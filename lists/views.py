from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Item
from .models import List

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(f'/lists/{list_.id}/')
        except ValidationError:
            item.delete()
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list' : list_, 'error' : error})

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text = request.POST.get('item_text', ''), list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', { 'error' : error })
    return redirect(f'/lists/{list_.id}/')
