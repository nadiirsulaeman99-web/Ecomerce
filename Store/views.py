import logging

from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchRank, SearchVector, SearchQuery
from .models import Product, Category
from cart.forms import CartAddProductForm
from django.core.cache import cache

from django.core.paginator import Paginator 

from cart.views import cart_add, cart_remove, cart_detial

from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.core.paginator import Paginator
from Store.models import Product, Category
from cart.forms import CartAddProductForm  # Hubi magaca galka form-kaaga cart-ka

from django.db.models import Prefetch

from django.contrib.auth.decorators import login_required
from django.db.models import Q


# list of all products
def home(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    cache_key = 'all_products'
    all_products = cache.get(cache_key)

    if all_products is None:
        all_products = Product.objects.all().filter(status=Product.Status.AVAILABLE)
        cache.set(cache_key, all_products, timeout=60*30)
        
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        all_products = all_products.filter(category=category)
    
    paginator = Paginator(all_products, 12)
    page_num  = request.GET.get('page')
    page_obj  = paginator.get_page(page_num)
    nums      = 'a' * page_obj.paginator.num_pages
    # Waxaan ku dhex dareynaa alaab kasta oo bogga hadda saaran foomkeeda "Add to Cart"
    for product in page_obj:
        product.cart_product_form = CartAddProductForm()
    
    # random list of products for the sidebar
    random_products = Product.objects.filter(status=Product.Status.AVAILABLE).select_related('category').order_by('?')
        
    context = {
        'categories': categories,
        'all_products': all_products,
        'category': category,
        'page_obj': page_obj,
        'nums': nums,
        'random_products': random_products,
    }
    
    return render(request, 'pages/home.html', context)

@login_required(login_url='acounts:login')
def product_detail(request, product_slug):
    cache_key = f'product_{product_slug}'
    product = cache.get(cache_key)
    if product is None:
        product = get_object_or_404(Product, slug=product_slug , status= Product.Status.AVAILABLE)
        cache.set(cache_key, product, timeout=60*30 )
    cart_add_form = CartAddProductForm
    context = {
        'detail':product,
        'cart_add_form':cart_add_form ,
        }
    return render(request, 'pages/details.html', context)


def search(request):
    query = None
    results = []
    
    if 'query' in request.GET:
        query = request.GET.get('query', '').strip()
        if not query:
            return redirect('Store:home')  # Haddii query-ga uu madhan yahay, dib ugu laabo homepage-ka
        
        if query:
            parsed_query = f"{query}:*"
            search_query = SearchQuery(parsed_query, search_type='raw')
            search_vector = SearchVector('name', 'description')
            
            results = Product.objects.annotate(
                search=search_vector, 
                rank=SearchRank(search_vector, search_query)
            ).filter(
                search=search_query, 
                status=Product.Status.AVAILABLE
            ).order_by('-rank')

    context = {
        'query': query,
        'results': results
    }
    return render(request, 'pages/search.html', context)



def page404(request, exception):
    return render(request, 'page404.html' ,  status=404)