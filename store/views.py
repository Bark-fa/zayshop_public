from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator
from store.models import Product
from cart.models import Item
from authentication.models import User

ids = []


def index(request):
    products = Product.objects.order_by('-list_date')[:3]
    return render(request, 'index.html', {'products': products})


def about(request):
    return render(request, 'about.html')


def constructQuery(getData, defaultQuery=False):
    values = {getData.GET.get("size"): True, 'genders': getData.GET.get('gender')}
    arguments = {}

    for key, val in values.items():
        if key and val:
            arguments[key] = val

    if getData.GET.get('search'):
        products = Product.objects.filter(
            Q(name__icontains=getData.GET.get('search').strip()) | Q(description__icontains=getData.GET.get('search').strip()),
            **arguments)

    else:
        if defaultQuery:
            products = Product.objects.all().order_by('-list_date')
        else:
            products = Product.objects.filter(**arguments)

    if getData.GET.get('price') == 'lth':
        products = products.filter(**arguments).order_by('price')

    elif getData.GET.get('price') == 'htl':
        products = products.filter(**arguments).order_by('-price')

    return products


def collectCartItems(req, prods):
    """ This function gets all the cart items from the user's cart because the templates use the index of
    cart items to decide whether to show a red remove button or a green add button when a user hovers over an item on
    the main page, the cart items are in a separate model of their own with a relationship to the product,
    therefore the item ID may be different from the actual product ID, that's why we first query the items from the current user's cart
    and then run a for loop to gather the id of every product from the cart entry that relates to it
    and then get the products that were passed to the function and check if any of them match a product ID in array ids
    if they do match, then we append that ID"""

    cartIds = []

    items = Item.objects.filter(user=req.user)
    for cartItem in items:
        cartIds.append(cartItem.product.id)

    for product in prods:
        if product.id in cartIds:
            ids.append(product.id)


def shop(request):
    is_filter_request = False

    # if any of the below GET values exist, it means that a user has applied filters to the products
    if request.GET.get("size") or request.GET.get('gender') or request.GET.get('price'):
        products = constructQuery(request)
        is_filter_request = True
    else:
        # if not, then return the products with the default sorting
        products = constructQuery(request, True)

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    # explaining what happens if we don't delete indexes is going to be a bit long, so go ahead and remove del ids[:] and see for yourself
    # don't say I didn't warn you though
    del ids[:]

    if request.user.is_authenticated:
        collectCartItems(request, products)

    # only return the partial if the user clicked on a filter button (price, gender, etc...) instead of re-rendering the entire template
    if is_filter_request:
        if ids:
            return render(request, 'products.html', {'products': paged_products, 'ids': ids, 'menu': request.GET.get('menu')})
        return render(request, 'products.html', {'products': paged_products, 'menu': request.GET.get('menu')})

    # if the page was requested without any filters applied
    if ids:
        return render(request, 'shop.html', {'products': paged_products, 'ids': ids})
    return render(request, 'shop.html', {'products': paged_products})


def contact(request):
    return render(request, 'contact.html')


def item(request, productid):
    product = get_object_or_404(Product, pk=productid)
    isInCart = False

    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)

        if Item.objects.filter(product=product, user=user).exists():
            isInCart = True
            item = get_object_or_404(Item, product=product, user=user)
            return render(request, 'item.html', {'product': product, 'inCart': isInCart, "item":item})

    return render(request, 'item.html', {'product': product, 'inCart': isInCart})
