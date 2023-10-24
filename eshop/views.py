from django.shortcuts import render ,redirect
from .models import *
from django.http import JsonResponse
import json
from .form import ShippingForm , CreateUserForm
# Authentication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout

from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# -------------------------Authentication Purpose--------------------------------------
def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                gustusername = form.cleaned_data.get('username')
                messages.success(request,'Account created for ' +' ' + gustusername)
                return redirect('login')
            
        context = {'form':form}
        return render(request, 'accounts/register.html',context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
            
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None: 
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,'Username or Passsword is incorrect!')

        return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')
# -------------------------Authentication Purpose End--------------------------------------


def home(request):
    
    if request.user.is_authenticated:
        profile = Customer.objects.get_or_create(user=request.user)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        item = []
        order = {'get_cart_total':0 , 'get_cart_items':0}
        cartItems = order['get_cart_items']
    
    obj = ComputerDetail.objects.all()
    context = {
        'obj': obj,
        'cartItems':cartItems,
    }
    return render(request,'home.html',context)

def detail(request,p_id):
        
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = []
        order = {'get_cart_total':0 , 'get_cart_items':0}
        cartItems = order['get_cart_items']


    obj1 = ComputerDetail.objects.get(id=p_id)

    context = {
        'obj':obj1,
        'cartItems':cartItems,
    }
    return render(request,'detail.html',context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        item = []
        order = {'get_cart_total':0 , 'get_cart_items':0}
        cartItems = order['get_cart_items']

    return render(request,'cart.html',{'item':item,
                                      'order':order,
                                       'cartItems':cartItems })

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:', productId)

    customer = request.user.customer
    product = ComputerDetail.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
   

def addtocart(request,cart_id):

    cart_obj = ComputerDetail.objects.get(id=cart_id)
    return render(request,'cart.html',{'cart_obj':cart_obj})


def search_item(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = []
        order = {'get_cart_total':0 , 'get_cart_items':0}
        cartItems = order['get_cart_items']

    if request.method == 'POST':
        searched = request.POST['searched']
        computers = ComputerDetail.objects.filter(name__contains=searched)

        context = {'searched': searched,
                   'computers':computers,
                   'cartItems':cartItems,}
        return render(request, 'search.html',context)
    else:
        
        return render(request, 'search.html',)
    
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        item = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        item = []
        order = {'get_cart_total':0 , 'get_cart_items':0}
        cartItems = order['get_cart_items']
    
    check = ShippingAddress.objects.all()

    shipping = ShippingForm()
    if request.method == 'POST':
        shipping = ShippingForm(request.POST)
        if shipping.is_valid():
            shipping.save()
        else:
            shipping = ShippingForm()
    context = {'item': item,
                    'order':order,
                    'cartItems':cartItems,
                    'check':check,
                    'shipping':shipping,}
    
    return render(request, 'checkout.html', context)

@login_required(login_url='login')
def pay(request):
    return render(request, 'paymentinfo.html')


