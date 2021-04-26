from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Item, Product, User


# Ignore the unnecessary elses after returns, they are there for readability purposes as some functions can get a bit long.

@login_required()
def index(request, calledFromRemove=False):
    items = Item.objects.filter(user=request.user)
    subtotal = 0

    for item in items:
        subtotal += item.product.price

    if calledFromRemove:
        return render(request, "cart_items.html", {"items": items, "subtotal": subtotal})

    return render(request, "cart.html", {"items": items, "subtotal": subtotal})


@login_required()
def add(request):
    if request.method == "POST":
        itemId = request.POST.get("id")
        quantity = request.POST.get("quantity")
        size = request.POST.get("size")
    else:
        if request.GET.get("add") == "false":
            remove(request)
            return HttpResponse()
        itemId = request.GET.get("id")
        quantity = 1
        size = 'S'

    product = Product.objects.get(pk=itemId)
    user = User.objects.get(pk=request.user.id)
    if Item.objects.filter(product=product, user=user).exists():
        return HttpResponse()
    else:
        item = Item(product=product, user=user, quantity=quantity, size=size)
        item.save()
        user.user.items_in_cart += 1
        user.save()

        return HttpResponse()


@login_required()
def remove(request):
    user = User.objects.get(pk=request.user.id)

    if request.method == "POST":
        itemId = request.POST.get("id")
    else:
        itemId = request.GET.get("id")
        if request.GET.get("add") == "true":
            add(request)
            return HttpResponse()

    product = Product.objects.get(pk=itemId)
    if Item.objects.filter(product=product, user=user).exists():
        Item.objects.filter(product=product, user=user).delete()
        user.user.items_in_cart -= 1
        user.save()

        if request.method == "GET":
            return index(request, True)
        return HttpResponse()

    return HttpResponse()


@login_required()
def decreaseQuantity(request):
    product = Product.objects.get(pk=request.GET.get("id"))

    # to avoid the server returning an error
    if Item.objects.filter(product=product, user=request.user).exists():

        # to get the item
        item = get_object_or_404(Item, product=product, user=request.user)

        if item.quantity != 1:
            item.quantity -= 1
            item.save()

    return HttpResponse()


@login_required()
def increaseQuantity(request):
    product = Product.objects.get(pk=request.GET.get("id"))

    # to avoid the server returning an error
    if Item.objects.filter(product=product, user=request.user).exists():
        # to get the item
        item = get_object_or_404(Item, product=product, user=request.user)

        item.quantity += 1
        item.save()

    return HttpResponse()


@login_required()
def changeSize(request, size):
    product = Product.objects.get(pk=request.GET.get("id"))
    if Item.objects.filter(product=product, user=request.user).exists():
        item = get_object_or_404(Item, product=product, user=request.user)
        item.size = size
        item.save()
        return HttpResponse()

    return HttpResponse()
