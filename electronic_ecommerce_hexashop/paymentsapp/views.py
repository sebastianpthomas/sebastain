from django.shortcuts import render
import stripe
from django.conf import settings
from django.views import View
from django.http import JsonResponse,HttpResponse
from django.views.generic import TemplateView
from customer.models import *
from django.views.decorators.csrf import csrf_exempt

stripe.api_key=settings.STRIPE_SECRET_KEY 

def SuccessView(request):
    return render(request, "success.html")

class CancelView(TemplateView):
    template_name='cancel.html'   

# class CreateCheckoutSessionView(View):

#     def post(self,request,*args,**kwargs):
#         YOUR_DOMAIN="http://127.0.0.1:8000"
#         user=request.user
#         cart = Cart.objects.filter(user=request.user, oredered=False)[:1].get()
#         cart_items = CartItems.objects.filter(cart=cart)
#         total = 50
#         for item in cart_items:
#             total+=item.product.price
#         grand_total=total*100
#         checkout_session = stripe.checkout.Session.create(
#             line_items=[
#                 {
#                    'price_data':{
#                     'currency':'usd',
#                     'unit_amount':10000,
#                     'product_data':{
#                         'name':'Testing'
#                     },
#                    },
#                    'quantity':1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN+'/payments' + '/success/',
#             cancel_url=YOUR_DOMAIN +'/payments' +  '/cancel/',
#         )
#         return JsonResponse({
#             'id':checkout_session.id
#         })

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        YOUR_DOMAIN1='http://'+request.META['HTTP_HOST']
        user = request.user
        cart = Cart.objects.filter(user=request.user, oredered=False)[:1].get()
        cart_items = CartItems.objects.filter(cart=cart)
        total = 50
        line_items = []
        for item in cart_items:
            total += item.product.price
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(item.product.price * 100),
                    'product_data': {
                        'name': item.product.name
                    },
                },
                'quantity': item.quantity,
            })
        grand_total = int(total)
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            metadata={
           'user':user.id

            },
            mode='payment',
            # success_url=YOUR_DOMAIN + '/payments' + '/success/',
            success_url='http://52.5.43.140:8006' + '/payments' + '/success/',
            cancel_url='http://52.5.43.140:8006' + '/payments' + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })

@csrf_exempt
def stripe_webhook(request):
  payload = request.body

  # For now, you only need to print out the webhook payload so you can see
  # the structure.
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, 'whsec_fd8cff64bd1cf0dde619025e9731b468eb9b02dbebfc02a38159ea88b3832404'
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
    session = stripe.checkout.Session.retrieve(
      event['data']['object']['id'],
      expand=['line_items'],
    )

    line_items = session.line_items
    # Fulfill the purchase...
    user=session['metadata']['user']
    cart = Cart.objects.get(user=user, oredered=False)
    cart.oredered = True
    cart.save()
    
  # Passed signature verification
  return HttpResponse(status=200)
