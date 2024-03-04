from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import shoes,Customer,Cartitem,ShippingAddress,Order,OrderItem,gymandaccessories,Winter,Tshirt,MotorSport
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from .forms import ShippingAddressForm,SetDeliveryAddressForm
from django.urls import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
from .forms import CreateUserForm
import razorpay
# Create your views here.
def shoe(request):
  s=shoes.objects.all()
  return render(request,'shoe.html',{'s':s})

def stepin(request):
  return render(request,'stepin.html')

def cricket(request):
  return render(request,'cricket.html')

def customer(request):
    return render(request,'customer.html')

def about(request):
  return render(request,'about.html')

def ney(request):
  data=shoes.objects.get(id=13)
  return render(request,'ney.html',{'data':data})

def neyvideo(request):
  return render(request,'neyvideo.html')

def shoe_details(request,id):
  data=shoes.objects.get(id=id)
  return render(request,'shoe_details.html',{'data':data})

# def signup(request):
#   if request.method=='POST':
#     fn=UserCreationForm(request.POST)
#     if fn.is_valid():
#       u = fn.save()
#       cus = Customer.objects.create(user=u)
#       cus.save()
#       print(cus)
#       return redirect('/')
#   else:
#     fn=UserCreationForm()
#     return render(request,'signup.html',{'form':fn})

def signup(request):
  fn=CreateUserForm()
  if request.method=='POST':
    fn=CreateUserForm(request.POST)
    if fn.is_valid():
      u = fn.save()
      cus = Customer.objects.create(user=u)
      cus.save()
    return redirect('/')
  else:
    fn=CreateUserForm()
    return render(request,'signup.html',{'form':fn})
  
def login_view(request):
  if request.method=='POST':
    fn=AuthenticationForm(request,data=request.POST)
    if fn.is_valid():
      uname=fn.cleaned_data['username']
      upass=fn.cleaned_data['password']
      u=authenticate(username=uname,password=upass)
      if u is not None:
        login(request,u)
        return redirect('/home')
  else:
    fn=AuthenticationForm()
  return render(request,'login_view.html',{'form':fn})

def search_result(request):
  query=request.GET.get('q')
  data=shoes.objects.filter(Q(sname__icontains=query) | Q(sprice__icontains=query))
  context={'data':data,'query':query}
  return render(request,'search.html',context)

def home(request):
  s=shoes.objects.all()
  return render(request,'home.html',{'s':s})

def add_to_cart(request,shoe_id):
    shoe=shoes.objects.get(id=shoe_id)
    customer=Customer.objects.get(user=request.user)
    existing_cart_items=Cartitem.objects.filter(customer__user=request.user,shoe=shoe)
    if len(existing_cart_items)==0:
        cart_item=Cartitem.objects.create(customer=customer,shoe=shoe)
    else:
        cart_item=existing_cart_items[0]
    cart_item.quantity=request.POST['quantity']
    cart_item.size=request.POST['size']
    cart_item.save()
    return redirect('cart_items')

def collect_cart_details(request):
    cart_items_list=Cartitem.objects.filter(customer__user=request.user)
    qty_list=[n for n in range(1, 6)]
    all_items_price=0
    for item in cart_items_list:
      if item.shoe is not None:
        item.item_price = item.quantity * item.shoe.sprice
        all_items_price += item.item_price
    else:
        pass

    context={
        'cart':cart_items_list,
        'total_price':all_items_price,
        'qty_list':qty_list
    }
    return context
  
def cart_items(request):
    context=collect_cart_details(request)
    return render(request,'cart_items.html', context=context)

def remove_from_cart(request,shoe_id):
    shoe=shoes.objects.get(id=shoe_id)
    cart_item=Cartitem.objects.get(customer__user=request.user.id,shoe=shoe)
    cart_item.delete()
    return redirect('cart_items')

def add_address(request):
    if request.method=='POST':
        form=ShippingAddressForm(request.POST)
        if form.is_valid():
            sd=form.save(commit=False)
            sd.customer=Customer.objects.get(user__id=request.POST['customer'])
            sd.save()
            return redirect("order_review",sa_id=sd.id)
    else:
        form=ShippingAddressForm()
    return render(request,'add_address.html',{'form':form})

def set_delivery_address(request):
    template_name="delivery_address.html"
    addr_list=ShippingAddress.objects.filter(customer__user__id=request.user.id)
    if request.method=="POST":
        form = SetDeliveryAddressForm(request.POST)
        if form.is_valid():
            return redirect('order_review',sa_id=form.cleaned_data['delivery_address'])
        else:
            form=SetDeliveryAddressForm()
        context={
            'address_list' : addr_list,
            'form':form
        }
        return render(request, template_name,context=context)
    
def order_review(request,sa_id):
    context=collect_cart_details(request)
    context['sa_id']=ShippingAddress.objects.get(id=sa_id)
    return render(request,'order_review.html',context=context)

def clear_cart_details(request):
    cart_items_list=Cartitem.objects.filter(customer__user=request.user)
    for item in cart_items_list:
        item.delete()

def checkout_order(request,sa_id):
    cart_items_list=collect_cart_details(request)['cart']
    customer=Customer.objects.filter(user=request.user)
    delivery_addr=ShippingAddress.objects.filter(id=sa_id)
    if customer:
        order=Order(customer=customer[0],
        shipping_address=delivery_addr[0])
        order.save()
        for item in cart_items_list:
            OrderItem.objects.create(
                order=order,
                product=item.shoe,
                price=item.shoe.sprice,
                quantity=item.quantity
            )
            clear_cart_details(request)
            request.session['order_id']=order.id
            return redirect(reverse('payment_order'))
        else:
            return redirect(reverse('shoe'))

def payment_order(request):
    order_id=request.session.get('order_id')
    print("process_order is",order_id)
    order=get_object_or_404(Order,id=order_id)
    amount=int(order.get_total_cost())
    amount_inr=amount*100
    context={
        'order_id':order_id,
        'public_key':settings.RAZOR_KEY_ID,
        'amount':amount_inr,
        'amountring':amount
    }
    return render(request,'created.html',context=context)

client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
def payment_process(request, order_id, amount):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.complete = True
        order.save()
        print("Amount ", amount)
        print("Type amount str to int ", amount)
        payment_id = request.POST['razorpay_payment_id']
        print("Payment Id", payment_id)
        order.transaction_id = payment_id
        order.save()
        payment_client_capture = (client.payment.capture(payment_id, amount))
        print("Payment Client capture", payment_client_capture)
        payment_fetch = client.payment.fetch(payment_id)
        status = payment_fetch['status']
        amount_fetch = payment_fetch['amount']
        amount_fetch_inr = amount_fetch
        print("Payment Fetch", payment_fetch['status'])
        context = {
            'amount': amount_fetch_inr,
            'status': status,
            'transaction_id': payment_id
        }
        return render(request, 'done.html', context=context)

def Gymandaccessories(request):
   g=gymandaccessories.objects.all()
   return render(request,'gymandacc.html',{'g':g})

def Gymandacc_details(request,gid):
  ga=gymandaccessories.objects.get(id=gid)
  return render(request,'gymandacc_details.html',{'ga':ga})

def add_to_cart_gym(request,gym_id):
    gym=gymandaccessories.objects.get(id=gym_id)
    customer=Customer.objects.get(user=request.user)
    existing_cart_items=Cartitem.objects.filter(customer__user=request.user,gym=gym)
    if len(existing_cart_items)==0:
        cart_item=Cartitem.objects.create(customer=customer,gym=gym)
    else:
        cart_item=existing_cart_items[0]
    cart_item.quantity=request.POST['quantity']
    cart_item.save()
    return redirect('cart_items_gym')

def collect_cart_details_gym(request):
    cart_items_list=Cartitem.objects.filter(customer__user=request.user)
    qty_list=[n for n in range(1, 6)]
    all_items_price=0
    for item in cart_items_list:
      if item.gym is not None:
        item.item_price = item.quantity * item.gym.price
        all_items_price += item.item_price
    else:
        pass

    context={
        'cart':cart_items_list,
        'total_price':all_items_price,
        'qty_list':qty_list
    }
    return context

def cart_items_gym(request):
    context=collect_cart_details_gym(request)
    return render(request,'cart_items_gym.html', context=context)

def remove_from_cart_gym(request,gym_id):
    gym=gymandaccessories.objects.get(id=gym_id)
    cart_item=Cartitem.objects.get(customer__user=request.user.id,gym=gym)
    cart_item.delete()
    return redirect('cart_items_gym')

def order_review_gym(request,sa_id):
    context=collect_cart_details_gym(request)
    context['sa_id']=ShippingAddress.objects.get(id=sa_id)
    return render(request,'order_review_gym.html',context=context)


def checkout_order_gym(request,sa_id):
    cart_items_list=collect_cart_details_gym(request)['cart']
    customer=Customer.objects.filter(user=request.user)
    delivery_addr=ShippingAddress.objects.filter(id=sa_id)
    if customer:
        order=Order(customer=customer[0],
        shipping_address=delivery_addr[0])
        order.save()
        for item in cart_items_list:
            OrderItem.objects.create(
                order=order,
                products=item.gym,
                price=item.gym.price,
                quantity=item.quantity
            )
            clear_cart_details(request)
            request.session['order_id']=order.id
            return redirect(reverse('payment_order'))
        else:
            return redirect(reverse('Gymandaccessories'))
        
def add_address_gym(request):
    if request.method=='POST':
        form=ShippingAddressForm(request.POST)
        if form.is_valid():
            sd=form.save(commit=False)
            sd.customer=Customer.objects.get(user__id=request.POST['customer'])
            sd.save()
            return redirect("order_review_gym",sa_id=sd.id)
    else:
        form=ShippingAddressForm()
    return render(request,'add_address.html',{'form':form})

def winter(request):
    w=Winter.objects.all()
    return render(request,'winter.html',{'w':w})

def winter_details(request,wid):
   w=Winter.objects.get(id=wid)
   return render(request,'winter_details.html',{'w':w})

def add_to_cart_winter(request,wid):
    winter=Winter.objects.get(id=wid)
    customer=Customer.objects.get(user=request.user)
    existing_cart_items=Cartitem.objects.filter(customer__user=request.user,winter=winter)
    if len(existing_cart_items)==0:
        cart_item=Cartitem.objects.create(customer=customer,winter=winter)
    else:
        cart_item=existing_cart_items[0]
    cart_item.quantity=request.POST['quantity']
    cart_item.size=request.POST['size']
    cart_item.save()
    return redirect('cart_items_winter')

def collect_cart_details_winter(request):
    cart_items_list=Cartitem.objects.filter(customer__user=request.user)
    qty_list=[n for n in range(1, 6)]
    all_items_price=0
    for item in cart_items_list:
      if item.winter is not None:
        item.item_price = item.quantity * item.winter.price
        all_items_price += item.item_price
    else:
        pass

    context={
        'cart':cart_items_list,
        'total_price':all_items_price,
        'qty_list':qty_list
    }
    return context

def cart_items_winter(request):
    context=collect_cart_details_winter(request)
    return render(request,'cart_items_winter.html', context=context)

def remove_from_cart_winter(request,wid):
    winter=Winter.objects.get(id=wid)
    cart_item=Cartitem.objects.get(customer__user=request.user.id,winter=winter)
    cart_item.delete()
    return redirect('cart_items_winter')

def order_review_winter(request,sa_id):
    context=collect_cart_details_winter(request)
    context['sa_id']=ShippingAddress.objects.get(id=sa_id)
    return render(request,'order_review_winter.html',context=context)


def checkout_order_winter(request,sa_id):
    cart_items_list=collect_cart_details_winter(request)['cart']
    customer=Customer.objects.filter(user=request.user)
    delivery_addr=ShippingAddress.objects.filter(id=sa_id)
    if customer:
        order=Order(customer=customer[0],
        shipping_address=delivery_addr[0])
        order.save()
        for item in cart_items_list:
            OrderItem.objects.create(
                order=order,
                productss=item.winter,
                price=item.winter.price,
                quantity=item.quantity
            )
            clear_cart_details(request)
            request.session['order_id']=order.id
            return redirect(reverse('payment_order'))
        else:
            return redirect(reverse('winter'))
        
def add_address_winter(request):
    if request.method=='POST':
        form=ShippingAddressForm(request.POST)
        if form.is_valid():
            sd=form.save(commit=False)
            sd.customer=Customer.objects.get(user__id=request.POST['customer'])
            sd.save()
            return redirect("order_review_winter",sa_id=sd.id)
    else:
        form=ShippingAddressForm()
    return render(request,'add_address.html',{'form':form})

def shirt(request):
    w=Tshirt.objects.all()
    return render(request,'shirt.html',{'w':w})

def shirt_details(request,wid):
   w=Tshirt.objects.get(id=wid)
   return render(request,'shirt_details.html',{'w':w})

def add_to_cart_shirt(request,wid):
    shirt=Tshirt.objects.get(id=wid)
    customer=Customer.objects.get(user=request.user)
    existing_cart_items=Cartitem.objects.filter(customer__user=request.user,shirt=shirt)
    if len(existing_cart_items)==0:
        cart_item=Cartitem.objects.create(customer=customer,shirt=shirt)
    else:
        cart_item=existing_cart_items[0]
    cart_item.quantity=request.POST['quantity']
    cart_item.size=request.POST['size']
    cart_item.save()
    return redirect('cart_items_shirt')

def collect_cart_details_shirt(request):
    cart_items_list=Cartitem.objects.filter(customer__user=request.user)
    qty_list=[n for n in range(1, 6)]
    all_items_price=0
    for item in cart_items_list:
      if item.shirt is not None:
        item.item_price = item.quantity * item.shirt.price
        all_items_price += item.item_price
    else:
        pass

    context={
        'cart':cart_items_list,
        'total_price':all_items_price,
        'qty_list':qty_list
    }
    return context

def cart_items_shirt(request):
    context=collect_cart_details_shirt(request)
    return render(request,'cart_items_shirt.html', context=context)

def remove_from_cart_shirt(request,wid):
    shirt=Tshirt.objects.get(id=wid)
    cart_item=Cartitem.objects.get(customer__user=request.user.id,shirt=shirt)
    cart_item.delete()
    return redirect('cart_items_shirt')

def order_review_shirt(request,sa_id):
    context=collect_cart_details_shirt(request)
    context['sa_id']=ShippingAddress.objects.get(id=sa_id)
    return render(request,'order_review_shirt.html',context=context)


def checkout_order_shirt(request,sa_id):
    cart_items_list=collect_cart_details_shirt(request)['cart']
    customer=Customer.objects.filter(user=request.user)
    delivery_addr=ShippingAddress.objects.filter(id=sa_id)
    if customer:
        order=Order(customer=customer[0],
        shipping_address=delivery_addr[0])
        order.save()
        for item in cart_items_list:
            OrderItem.objects.create(
                order=order,
                prod=item.shirt,
                price=item.shirt.price,
                quantity=item.quantity
            )
            clear_cart_details(request)
            request.session['order_id']=order.id
            return redirect(reverse('payment_order'))
        else:
            return redirect(reverse('shirt'))
        
def add_address_shirt(request):
    if request.method=='POST':
        form=ShippingAddressForm(request.POST)
        if form.is_valid():
            sd=form.save(commit=False)
            sd.customer=Customer.objects.get(user__id=request.POST['customer'])
            sd.save()
            return redirect("order_review_shirt",sa_id=sd.id)
    else:
        form=ShippingAddressForm()
    return render(request,'add_address.html',{'form':form})

def motor(request):
    w=MotorSport.objects.all()
    return render(request,'motor.html',{'w':w})

def motor_details(request,wid):
   w=MotorSport.objects.get(id=wid)
   return render(request,'motor_details.html',{'w':w})

def add_to_cart_motor(request,wid):
    ms=MotorSport.objects.get(id=wid)
    customer=Customer.objects.get(user=request.user)
    existing_cart_items=Cartitem.objects.filter(customer__user=request.user,ms=ms)
    if len(existing_cart_items)==0:
        cart_item=Cartitem.objects.create(customer=customer,ms=ms)
    else:
        cart_item=existing_cart_items[0]
    cart_item.quantity=request.POST['quantity']
    cart_item.size=request.POST['size']
    cart_item.save()
    return redirect('cart_items_motor')

def collect_cart_details_motor(request):
    cart_items_list=Cartitem.objects.filter(customer__user=request.user)
    qty_list=[n for n in range(1, 6)]
    all_items_price=0
    for item in cart_items_list:
      if item.ms is not None:
        item.item_price = item.quantity * item.ms.price
        all_items_price += item.item_price
    else:
        pass

    context={
        'cart':cart_items_list,
        'total_price':all_items_price,
        'qty_list':qty_list
    }
    return context

def cart_items_motor(request):
    context=collect_cart_details_motor(request)
    return render(request,'cart_items_motor.html', context=context)

def remove_from_cart_motor(request,wid):
    ms=MotorSport.objects.get(id=wid)
    cart_item=Cartitem.objects.get(customer__user=request.user.id,ms=ms)
    cart_item.delete()
    return redirect('cart_items_motor')

def order_review_motor(request,sa_id):
    context=collect_cart_details_motor(request)
    context['sa_id']=ShippingAddress.objects.get(id=sa_id)
    return render(request,'order_review_motor.html',context=context)


def checkout_order_motor(request,sa_id):
    cart_items_list=collect_cart_details_motor(request)['cart']
    customer=Customer.objects.filter(user=request.user)
    delivery_addr=ShippingAddress.objects.filter(id=sa_id)
    if customer:
        order=Order(customer=customer[0],
        shipping_address=delivery_addr[0])
        order.save()
        for item in cart_items_list:
            OrderItem.objects.create(
                order=order,
                prods=item.ms,
                price=item.ms.price,
                quantity=item.quantity
            )
            clear_cart_details(request)
            request.session['order_id']=order.id
            return redirect(reverse('payment_order'))
        else:
            return redirect(reverse('motor'))
        
def add_address_motor(request):
    if request.method=='POST':
        form=ShippingAddressForm(request.POST)
        if form.is_valid():
            sd=form.save(commit=False)
            sd.customer=Customer.objects.get(user__id=request.POST['customer'])
            sd.save()
            return redirect("order_review_motor",sa_id=sd.id)
    else:
        form=ShippingAddressForm()
    return render(request,'add_address.html',{'form':form})