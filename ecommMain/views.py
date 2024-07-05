from django.shortcuts import render

from StoreApp.models import Product
# Create your views here.

def index(request):
    products =Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request,'index.html',context)
        
    