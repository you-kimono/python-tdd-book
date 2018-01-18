from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Item
from .models import List

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items' : items})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text = request.POST.get('item_text', ''), list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
