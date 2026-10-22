from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator

def index(request):
    latestproduct=Product.objects.order_by('priority')[:4]
    Bigsale=Product.objects.order_by('-id')[:4]
    context={
         "latestproduct":latestproduct,
         "Bigsale":Bigsale
    }
    return render(request,"index.html",context)
def list_products(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    product_list=Product.objects.all()
    product_paginator=Paginator(product_list,4)
    product_list=product_paginator.get_page(page)
    return render(request,"products.html",{"products":product_list})


def product_detail(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,"product_detail.html",{"product":product})


