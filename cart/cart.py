from decimal import Decimal
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from .cart_exceptions import KeyNotSet, ModelDoesNotExist


CART_SESSION_KEY = getattr(settings, 'CART_SESSION_KEY', 'cart')
PRODUCT_MODEL = getattr(settings, 'PRODUCT_MODEL', 'Product')


class Cart(object):

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(CART_SESSION_KEY)

        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}

        self.cart = cart

    def add(self, product, price, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'price': int(price), 'quantity': 0}

        self.cart[product_id]['quantity'] = int(quantity)
        self.save()

    def save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()

        if PRODUCT_MODEL is not 'Product':
            splitted = str(PRODUCT_MODEL).split('.')
            if len(splitted) != 2:
                msg = 'PRODUCT_MODEL not in format: app_label.model_class'
                raise ImproperlyConfigured(msg)
            app_label = splitted[0]
            model = splitted[1]

            try:
                ct = ContentType.objects.get(app_label=app_label, model=model)
                model = ct.model_class()
            except ObjectDoesNotExist:
                msg = 'app \'{}\' does not have a \'{}\' model'
                msg = msg.format(app_label, model.capitalize())
                raise ModelDoesNotExist(msg)
        else:
            try:
                ct = ContentType.objects.get(model='product')
                model = ct.model_class()
            except ObjectDoesNotExist:
                msg = 'PRODUCT_MODEL missing in settings'
                raise KeyNotSet(msg)

        products = model.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart.values())

    @property
    def total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.session.cart[settings.CART_SESSION_KEY] = {}
        self.session.modified = True
