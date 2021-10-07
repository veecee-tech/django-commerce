from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart_Item
from cart.views import _cart_id
from store.models import Product, Category

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# from cart.models import Cart_Item
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available=True).order_by('-created_date')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-created_date')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,

    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = Cart_Item.objects.filter(cart__cart_id = _cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e
    
    context = {
        'in_cart': in_cart,
        'single_product': single_product
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    context = {}
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        
        if keyword:
            products = Product.objects.order_by('-created_date').filter(description__icontains=keyword)
            context = {
            'products': products,
            'product_count': products.count()
        }
        else: 
            pass
            
        
    return render(request, 'store/store.html', context)