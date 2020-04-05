"""views.py"""
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import generic
import stripe
from .models import Products, BuyingHistory
from .forms import ProductForm

# read APIKEY
with open(settings.BASE_DIR + '/shopping/api_setting/apikey.txt', mode='r') as file:
    stripe.api_key = file.read()
    print('stripe.api_key:', stripe.api_key)

def index(request):
    """いわばhtmlのページ単位の構成物です"""
    # htmlとして返却します
    return render(request, 'shopping/index.html')

class IndexView(generic.ListView):
    """IndexView"""
    template_name = 'shopping/index.html'
    model = Products
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """form"""
        context = super().get_context_data(**kwargs)
        context['form'] = ProductForm()
        return context

class DetailView(generic.DetailView):
    """DetailView"""
    template_name = 'shopping/detail.html'
    model = Products

    def post(self, request, *args, **kwargs):
        """post"""
        product = self.get_object()
        token = request.POST['stripeToken']  # 'stripeToken' will made by form submit
        try:
            # buy
            charge = stripe.Charge.create(
                amount=product.price,
                currency='jpy',
                source=token,
                description='メール:{} 商品名:{}'.format(request.user.email, product.name),
            )
        except stripe.error.CardError as error:
            # error: Payment was not successful. e.g. payment limit over
            context = self.get_context_data()
            context['message'] = error.error.message
            return render(request, 'shopping/product_detail.html', context)
        else:
            # ok
            BuyingHistory.objects.create(product=product, user=request.user, stripe_id=charge.id)
            return redirect('shp:index')

    def get_context_data(self, **kwargs):
        """STRIPE_PUBLIC_KEYを渡したいだけ"""
        context = super().get_context_data(**kwargs)
        context['public_key'] = settings.STRIPE_PUBLIC_KEY
        return context
