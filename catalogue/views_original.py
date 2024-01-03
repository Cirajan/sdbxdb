from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
from django.core.paginator import Paginator, InvalidPage
from .filters import ItemFilter
# Create your views here.


def home(request):

    items = Item.objects.all()

    itemfilter = ItemFilter(request.GET, queryset = items)
    items = itemfilter.qs
    items_count = items.count()


    p = Paginator(items, 10)
    page_num = request.GET.get('page', 1)


    try:
        page = p.page(page_num)
    except InvalidPage:
        page = p.page(1)


    path = ''
    path += "%s" % "&".join(["%s=%s" % (key, value) for (key, value) in request.GET.items() if not key=='page' ])

    # Split the page of items into two lists, one odd indexes the other even
    page_odds = []
    page_evens = []
    for i in range(len(page)):
        if i % 2: page_evens.append(page[i])
        else:
            page_odds.append(page[i])

    # Join the two lists into a zipped list of tuples
    zip_page = zip(page_odds, page_evens)

    context = {
        'page': page,
        'items': zip_page,
        'itemfilter': itemfilter,
        'path': path,
        'items_count': items_count,
        'page_num': page_num

    }
    return render(request, 'catalogue/home.html', context)
