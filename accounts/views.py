from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
#from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

# Create your views here.

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        redirect('home')
    context = {'form':form}
    return render(request,'accounts/register.html',context)

def loginPage(request):
    context = {}
    return render(request,'accounts/login.html',context)

def home(request):
    customerdata = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {
        "customerdata":customerdata,
        "orders":orders,
        "total_orders":total_orders,
        "delivered":delivered,
        "pending":pending,
    }
    return render(request,"accounts/dashboard.html",context)

def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    
    customer_total_orders = Order.objects.filter(customer=customer)
    ctoc = customer_total_orders.count()
    myFilter = OrderFilter(request.GET, queryset=customer_total_orders)
    customer_total_orders = myFilter.qs
    context = {
        "customer":customer,
        "customer_total_orders":customer_total_orders,
        "ctoc":ctoc,
        "myFilter":myFilter,
    }
    return render(request,'accounts/customer.html',context)

def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{"products":products})

def createOrder (request,pk):
    orderformset = inlineformset_factory(Customer,Order,fk_name="customer",fields=('product','status'),extra=4)
    customer = Customer.objects.get(id=pk)
    formset = orderformset(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = orderformset(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context = {'formset':formset,"customer":customer}
    return render(request, 'accounts/order_form.html',context)

def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        form.save()
        return redirect("home")
    context = {"form":form}
    return render(request,'accounts/order_form.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("home")
    context={"order":order}
    return render(request,'accounts/delete.html',context)
