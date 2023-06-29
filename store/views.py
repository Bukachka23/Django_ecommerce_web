from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.contrib.auth import login
from django.db.models import Q


# This view handles login requests. If the request method is POST, it tries to authenticate the user
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('store')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


# This view handles signup requests. If the request method is POST, it tries to create a new user
def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("web_store")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

    form = NewUserForm()
    return render(request=request, template_name="store/signup.html", context={"register_form":form})


# This view handles the 'store' page. It gets data related to the user's cart and queries for products
def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	query = request.GET.get('q')
	if query:
		products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
	else:
		products = Product.objects.all()

	context = {'products':products, 'cartItems':cartItems, 'order':order, 'items':items}
	return render(request, 'store/store.html', context)


# This view handles the 'cart' page. It gets data related to the user's cart
def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


# This view handles the 'checkout' page. It gets data related to the user's cart
def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)


# This view handles updates to the cart. It gets the product ID and action (add or remove) from the request body
# Based on the action, it either increments or decrements the quantity of the product in the user's cart
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


# This view handles the checkout process. If the user is authenticated, it gets the user's order
# If the user is not authenticated, it creates a guest order. It then checks if the total price is correct
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


# This view handles requests to view a single product. It gets the product by its ID and gets data related to the user's cart
def view_item(request, item_id):
	item = get_object_or_404(Product, pk=item_id)
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'items': items, 'products':products, 'cartItems':cartItems, 'item': item, 'order': order}
	return render(request, 'store/view_item.html', context)


# This view handles requests to the home page.
def home(request):
    return render(request, 'store/home.html')