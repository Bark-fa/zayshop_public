from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator
from store.models import Product
from cart.models import Item
from authentication.models import User

cartIds = []
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

    if getData.GET.get('search') and getData.GET.get('search') != "":
        products = Product.objects.filter(
            Q(name__icontains=getData.GET.get('search')) | Q(description__icontains=getData.GET.get('search')),
            **arguments)

    else:
        if defaultQuery:
            products = Product.objects.all().order_by('list_date')
        else:
            products = Product.objects.filter(**arguments)

    if getData.GET.get('price') == 'lth':
        products = products.filter(**arguments).order_by('price')

    elif getData.GET.get('price') == 'htl':
        products = products.filter(**arguments).order_by('-price')

    return products


def updateShop(request):
    products = constructQuery(request)

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    if request.user.is_authenticated:
        del cartIds[:]
        collectCartItems(request, products)
    if cartIds:
        del cartIds[:]
        return render(request, 'products.html',
                      {'products': paged_products, 'ids': ids, 'menu': request.GET.get('menu')})  
    return render(request, 'products.html', {'products': paged_products, 'menu': request.GET.get('menu')})


def collectCartItems(req, prods):
    del cartIds[:]
    del ids[:]
    items = Item.objects.filter(user=req.user)
    for cartItem in items:
        cartIds.append(cartItem.product.id)

    for product in prods:
        if product.id in cartIds:
            ids.append(product.id)


def shop(request):
    products = constructQuery(request, True)

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    del ids[:]
    if request.user.is_authenticated:
        collectCartItems(request, products)
    if cartIds:
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
