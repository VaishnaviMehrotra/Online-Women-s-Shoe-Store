import json

from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
# Create your views here.
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect
1from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
from basic.models import User, Stock, Cart


def error_response(message, status=500):
    error_response = {}
    error_response['message'] = message
    return HttpResponse(json.dumps(error_response), content_type='application/json', status=status)


def register(request):
    print("In signup !!!")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        request_body = json.loads(body_unicode)
        try:
            validate_email(request_body['email'])
        except ValidationError as exception:
            print(exception.message)
            error_message = 'Validation error!!!'
            if ('valid email address' in exception.message):
                error_message = 'Email address is not valid !!! Please try valid email address.'
            return error_response(error_message, 400)

        user = User.objects.create_user(request_body['email'])
        user.set_password(request_body['pwd'])
        user.first_name = request_body['first_name']
        user.last_name = request_body['last_name']
        user.phone_number = request_body['phone_number']
        user.birthday = request_body['birthday']
        user.country = request_body['country']
        user.save()
        request.session['username'] = request_body['email']

    return render(request, 'registration.html')

def purchase(request):

    print("In signup !!!")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        request_body = json.loads(body_unicode)
        try:
            validate_email(request_body['email'])
        except ValidationError as exception:
            print(exception.message)
            error_message = 'Validation error!!!'
            if ('valid email address' in exception.message):
                error_message = 'Email address is not valid !!! Please try valid email address.'
            return error_response(error_message, 400)

        user.card_number = request_body['card_number']
        user.cv_code = request_body['cv_code']
        user.expiration_date = request_body['expiration_date']
        user.amount= request_body['amount']
        user.save()
        request.session['username'] = request_body['email']

    return render(request, 'purchase.html')

def index(request):
    loggedIn=False
    if request.session.has_key('username'):
        loggedIn=True
    return render(request, 'index.html', {'loggedIn': loggedIn})

def about(request):
    loggedIn = False
    if request.session.has_key('username'):
        loggedIn = True
    return render(request, 'about.html', {'loggedIn': loggedIn})

def stock(request):
    # context = {}
    store = Stock.objects.filter(type="Stock")
    # context["items"] = product
    loggedIn = False

    if request.session.has_key('username'):
        loggedIn = True

    # store = Stock.objects.all()
    specs = []

    print(store)
    for store_vsl in store:
        specs.append(store_vsl.store.split(","))
        print(store_vsl.price)
        print(store_vsl.img1)
        print(store_vsl.img2)
        print(store_vsl.img3)
        print(store_vsl.img4)
        print(store_vsl.img5)
        print(store_vsl.store)

    return render(request, 'stock.html', {'stores': store, 'loggedIn': loggedIn, 'specs': specs})

def contact(request):
    loggedIn = False
    if request.session.has_key('username'):
        loggedIn = True
    return render(request, 'contact.html', {'loggedIn': loggedIn})


def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        request_body = json.loads(body_unicode)
        email = request_body['email']
        pwd = request_body['pwd']

        print(email)
        print(pwd)

        filtered_account = authenticate(username=email, password=pwd)
        if filtered_account:
            request.session['username'] = email
        else:
            return HttpResponse("status code is not correct", status=500)

        return HttpResponse("success", status=200)


    return render(request, 'login.html')


def removeCartItem(request):
    print("In the remove cart item.")
    item_id = request.GET.get("id")
    print(item_id)
    Cart.objects.filter(id=item_id, user__email=request.user.email).delete()
    return HttpResponse("success")

def cart(request):
    context = {}
    product = Cart.objects.filter(user__email=request.user.email, status=False)
    context["items"] = product
    print('In the context')
    #loggedIn = False
    #if request.session.has_key('username'):
     #   loggedIn = True
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST.get("qty"))
            print(request.POST.get("pid"))
            pid = request.POST["pid"]
            qty = request.POST["qty"]
            print(request.user)
            print(pid)
            user_id = User.objects.get(email=request.user).email
            print(user_id)

            is_exist = Cart.objects.filter(product__id=pid, user__email=request.user.email, status=False)

            if len(is_exist) > 0:
                context["msz"] = "Item Already Exists in Your Cart"
                context["cls"] = "alert alert-warning"
            else:
                product = get_object_or_404(Stock, id=pid)
                usr = get_object_or_404(User, email=request.user.email)
                c = Cart(user=usr, product=product, quantity=qty)

                c.save()
                context["msz"] = "{} Added in Your Cart".format(product.name)
                context["cls"] = "alert alert-success"
    else:
        context["status"] = "Please Login First To View Your Cart"
    return render(request, "cart.html", context)
    #return render(request, 'cart.html', {'loggedIn': loggedIn})
'''def cart_page(request):
    cart_obj, cart_new = Cart.objects.new_or_get(request=request)
    return render(request, 'carts/cart.html', {'cart': cart_obj})

def cart_update(request):
    product_id = request.POST.get("product_id", None)
    if product_id:
        product_obj = Product.objects.get(id=product_id)
        if not product_obj:
            return Product.DoesNotExist
        cart_obj, cart_new = Cart.objects.new_or_get(request=request)
        purchases = ProductPurchase.objects.purchased(request)
        already_purchased = product_obj in purchases
        if already_purchased:
            messages.success(request, 'product was already purchased')
            return redirect('purchases')
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            removed = True
            added = False
        else:
            cart_obj.products.add(product_obj)
            removed = False
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            return JsonResponse({"added":added,
                                 "removed": removed,
                                 "cart_count": cart_obj.products.count()})
        return redirect('carts:cart')
def cart_api_update(request):
    resp = {}
    cart_obj, cart_new = Cart.objects.new_or_get(request=request)
    products = [{'name': p.name, 'price': p.price, 'url': p.get_absolute_url()} for p in cart_obj.products.all()]
    resp['products'] = products
    resp['total'] = cart_obj.total
    return JsonResponse(resp)
'''

def heels(request):
    # context = {}
    store = Stock.objects.filter(type="Heels")
    # context["items"] = product
    loggedIn = False
    if request.session.has_key('username'):
        loggedIn = True
    # store = Heels.objects.all()
    print(store)
    for store_vsl in store:
        print(store_vsl.price)
        print(store_vsl.img1)
        print(store_vsl.img2)
        print(store_vsl.img3)
        print(store_vsl.img4)
        print(store_vsl.img5)
        print(store_vsl.store)
    return render(request, 'Heels.html', {'stores': store, 'loggedIn': loggedIn})

def casualShoes(request):
    #context = {}
    store = Stock.objects.filter(type="CasualShoes")
    #context["items"] = product
    loggedIn = False
    if request.session.has_key('username'):
        loggedIn = True

    #store = CasualShoes.objects.all()
    print(store)
    for store_vsl in store:
        print(store_vsl.price)
        print(store_vsl.img1)
        print(store_vsl.img2)
        print(store_vsl.img3)
        print(store_vsl.img4)
        print(store_vsl.img5)
        print(store_vsl.store)
    return render(request, 'Casual-Shoes.html', {'stores': store, 'loggedIn': loggedIn})

def boots(request):
    #context = {}
    store = Stock.objects.filter(type="Boots")
    #context["items"] = product
    loggedIn = False
    loggedIn = False
    print(store)
    if request.method == "POST":
     if request.session.has_key('username'):
      loggedIn = True

    #store = Boots.objects.all()
    print(store)
    for store_vsl in store:
        print(store_vsl.price)
        print(store_vsl.img1)
        print(store_vsl.img2)
        print(store_vsl.img3)
        print(store_vsl.img4)
        print(store_vsl.img5)
        print(store_vsl.store)
        print(store_vsl.id)
    return render(request, 'Boots.html', {'stores': store, 'loggedIn': loggedIn})

def sportsShoesANDFloaters(request):
    #context = {}
    store = Stock.objects.filter(type="SportsShoesANDFloaters")
    #context["items"] = product
    loggedIn = False
    loggedIn = False
    if request.session.has_key('username'):
        loggedIn = True

    #store = SportsShoesANDFloaters.objects.all()
    print(store)
    for store_vsl in store:
        print(store_vsl.price)
        print(store_vsl.img1)
        print(store_vsl.img2)
        print(store_vsl.img3)
        print(store_vsl.img4)
        print(store_vsl.img5)
        print(store_vsl.store)
    return render(request, 'SportsShoes&Floaters.html', {'stores': store, 'loggedIn': loggedIn})

def logout_view(request):
    if(request.session.has_key('username')):
        del request.session['username']
    logout(request)
    print('User is logged out!!!')
    return HttpResponseRedirect('/index')

#def AddProduct(request):
 #   if(request.session.has_key('username')):
  #      del request.session['username']
   # logout(request)
    #print('Add to Product!!!')
    #return HttpResponseRedirect('/index')

def get_cart_data(request):
    product = Cart.objects.filter(user__email=request.user.email, status=False)
    total, qty = 0, 0
    for store in product:
        print(float(store.product.price))
        total += float(store.product.price)
        qty += int(store.quantity)
    print(total)
    print(qty)
    res = {
        "total": total, "quan": qty,
    }
    return JsonResponse(res)

def change_quan(request):
    cid = request.GET["cid"]
    qty = request.GET["quantity"]
    cart_obj = get_object_or_404(Cart, id=cid)
    cart_obj.quantity = qty
    cart_obj.save()
    return HttpResponse(1)