=====
Django-Kart
=====

Django-Kart is a simple app to incorporate session-based carts to your Django app. 
Djago-Kart has been tested for Django >= 1.8



Installation
-----------

1. Install using `pip`:
    pip install django-kart

2. Add "cart" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'cart',
    ]

3. By default, django-kart assumes a Product model named `Product`. It is advisable to set `PRODUCT_MODEL` in your settings.py:
    PRODUCT_MODEL = 'app.model' 

4. Django-kart looks for a `cart` key in session. You can overwrite this by setting `CART_SESSION_KEY` to a string:
    CART_SESSION_KEY = 'new_key' 


Usage
-----------

```python
# views.py
from django.shortcuts import get_object_or_404
from cart.cart import Cart
from app.models import Product

def cart_add(request, slug):
    product = get_object_or_404(Product, slug=slug)
    quantity = request.POST.get(quantity)
    cart = Cart(request)
    cart.add(product, product.price, quantity)

def cart_remove(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)
    cart.remove(product)

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})
```

```django
# templates/cart.html
{% extends 'base.html' %}

{% block body %}
    <div class="container">
        <h4>Items in cart {{cart | length}}</h4>
        {% for item in cart %}
            <p>{{item.name}}</p>
            <p>${{item.price}}</p>
            <form method="POST" action="{% url 'cart_add' item.product.id %}">
                {% csrf_token %}
                <div class="form-group">
                    <input type="number" value="{{item.quantity}}" max="{{item.stock}}"
                        class="form-control" min="1" name="quantity">
                    <input type="submit" value="Update" class="btn btn-primary">
                </div>
            </form>
        {% endfor %}
    </div>
{% endblock %}
```

Inspirations
-----------

This project draws from three resources:
* [django-carton](https://github.com/lazybird/django-carton "django-carton")
* [django-cart](https://raw.githubusercontent.com/bmentges/django-cart "django-cart")
* [LinkedIn](https://www.linkedin.com/learning/django-3-building-an-online-shop/ "LinkedIn Learning")