from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from StoreApp.models import (Product,Variation)
from CategoryApp.models import Category
from CartsApp.models import CartItem
from CartsApp.views import _cart_id
# using paginator library
from django.core.paginator import (EmptyPage,PageNotAnInteger, Paginator)
# Create your views here.


def store(request,category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug= category_slug)
        products = Product.objects.filter(category=categories,is_available=True).order_by('id')       
        #---------------------- paginator code start from here ----------------------
        paginator = Paginator(products , 3)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        #---------------------- paginator code end from here ----------------------
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        #---------------------- paginator code start from here ----------------------
        paginator = Paginator(products , 3)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        #---------------------- paginator code end from here ----------------------

        products_count = products.count()
        
    context = {
        'products': page_products,
        'products_count': products_count,
    }
    return render(request,'StoreApp/store.html',context)


def product_details(req,  category_slug,  product_slug):
    try:
        single_product = Product.objects.get(category__slug= category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(req), product= single_product).exists()
    except Exception as E:
        raise E
    
    context = {
        'single_product': single_product,
        'in_cart' : in_cart,
    }

    return render(req,'StoreApp/product_details.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-create_at').filter(Q(brief_description__icontains= keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()

    context = {
        'products':products,
        'products_count':products_count,
        }
    return render(request,'StoreApp/store.html',context)















