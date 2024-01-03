from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, Category
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.decorators import login_required
from .filters import ItemFilter
# Create your views here.

@login_required
def home(request):

    # Generate list of categories to pass in context for drop down options
    categories = Category.objects.all()


    # Get the search terms from url GET info field and filter items based on results
    content_contains = request.GET.get('contentContains')
    category_selection = request.GET.getlist('category')
    # category_contains = request.GET.get('categoryContains')

    # Generate a full list of all items for filtering
    items = Item.objects.all()


    # Determine state of search fields and create filters accordingly
    if content_contains is None and not category_selection:
        pass
    elif content_contains != '' and content_contains is not None and category_selection[0] == '':
        items = items.filter(contents__icontains=content_contains)
    elif content_contains == '' and category_selection[0] != '':
        items = items.filter(category__name__in=category_selection)
    elif content_contains != '' and category_selection[0] != '':
        items = items.filter(contents__icontains=content_contains).filter(category__name__in=category_selection)



    items_count = items.count()


    p = Paginator(items, 10)
    page_num = request.GET.get('page', 1)


    try:
        page = p.page(page_num)
    except InvalidPage:
        page = p.page(1)

    # Extract search criteria (not page) from GET request url and process in path variable to pass to template.
    # Necessary to maintain search criteria during pagination




    search_terms = []

    if not content_contains:
        search_terms.append(('contentContains', ''))
    else:
        search_terms.append(('contentContains', content_contains))

    if not category_selection:
        search_terms.append(('category', ''))
    else:
        for c in category_selection:
            search_terms.append(('category', c))


    path = ''
    # path += "%s" % "&".join(["%s=%s" % (key, value) for (key, value) in request.GET.items() if not key=='page' ])
    path += "%s" % "&".join(["%s=%s" % (key, value) for (key, value) in search_terms])
    print(path)

    # If number of returned items from search is odd, remove last item and pass it separately to the template.
    # This is necessary due to jinja 2 being unable to iterate over a zipped list element if one entry in element is empty
    last_item_if_odd = None
    page_list = list(page)
    if not page.has_next():
        if (len(page_list) % 2) != 0:
            last_item_if_odd = page_list.pop()



    # Split the page_list of items into two lists, one odd indexes the other even
    page_odds = []
    page_evens = []
    for i in range(len(page_list)):
        if i % 2: page_evens.append(page_list[i])
        else:
            page_odds.append(page_list[i])

    # Join the two lists into a zipped list of tuples
    zip_page = zip(page_odds, page_evens)



    context = {
        'categories': categories,
        'page': page,
        'items': zip_page,
        'last_item_if_odd': last_item_if_odd,
        'path': path,
        'items_count': items_count,
        'page_num': page_num
    }
    return render(request, 'catalogue/home.html', context)
