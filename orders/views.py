from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from django.views import generic

from .models import Category, Pricing, Cart, CartItem

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'orders/index.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """Return the categories sorted by order_nr"""
        return Category.objects.order_by('order_nr')


class CartView(generic.DetailView):
    model = Cart
    
    def get_object(self):
        if not self.request.session.has_key('cart_id'):
            return None
        cart_id = self.request.session['cart_id']
        return Cart.objects.get(pk=cart_id)


@require_http_methods(["POST"])
def add_to_cart(request):
    pricing_id = int(request.POST['pricing_id'])
    pricing_item = Pricing.objects.get(pk=pricing_id)
    if request.session.has_key('cart_id'):
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(pk=cart_id)
        cart.cartitem_set.add(CartItem(pricing_item=pricing_item), bulk=False)
        cart.save()
    else:
        cart = Cart()
        cart.save()
        cart.cartitem_set.add(CartItem(pricing_item=pricing_item), bulk=False) # pylint: disable=E1101
        cart.save()
        request.session['cart_id'] = cart.pk
    return HttpResponseRedirect(reverse('orders:cart'))


@require_http_methods(["POST"])
def delete_cart(request):
    cart_id = request.session['cart_id']
    cart = Cart.objects.get(pk=cart_id)
    cart.is_deleted = True
    cart.save()
    del request.session['cart_id']
    return HttpResponseRedirect(reverse('orders:cart'))
